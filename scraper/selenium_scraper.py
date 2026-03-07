from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

from newspaper import Article
from urllib.parse import urlparse, urljoin
from datetime import datetime, timedelta
from dateutil import parser as dateparser
import json
import os
import time
from scraper.article_extractor import extract_article_with_fallback


def parse_date(date_str):
    if not date_str:
        return None
    try:
        return dateparser.parse(date_str, ignoretz=True)
    except (ValueError, TypeError):
        pass

    # Fallback: format Indonesia ("21 Juni 2024 | 12.00 WIB")
    try:
        bulan_id = {
            'januari': 'January', 'februari': 'February', 'maret': 'March',
            'april': 'April', 'mei': 'May', 'juni': 'June',
            'juli': 'July', 'agustus': 'August', 'september': 'September',
            'oktober': 'October', 'november': 'November', 'desember': 'December'
        }
        cleaned = date_str.split('|')[0].strip()
        cleaned = cleaned.replace(' WIB', '').replace(' WITA', '').replace(' WIT', '')
        for id_name, en_name in bulan_id.items():
            cleaned = cleaned.replace(id_name.capitalize(), en_name)
            cleaned = cleaned.replace(id_name, en_name)
        return dateparser.parse(cleaned, ignoretz=True)
    except (ValueError, TypeError):
        return None


def parse_input_date(text):
    text = text.strip().lower()
    today = datetime.now()
    if text in ('hari ini', 'today'):
        return today
    elif text in ('kemarin', 'yesterday'):
        return today - timedelta(days=1)
    try:
        return dateparser.parse(text, ignoretz=True)
    except (ValueError, TypeError):
        return None


def article_matches_date(article, start_date, end_date):
    dt = parse_date(article.get('date'))
    if not dt:
        return False
    return start_date.date() <= dt.date() <= end_date.date()


def build_date_urls(base_url, start_date, end_date):
    parsed = urlparse(base_url)
    domain = parsed.netloc.lower().replace('www.', '')

    # Mapping domain ke fungsi pembuat URL tanggal
    date_patterns = {
        # Detik: news.detik.com/indeks?date=MM/DD/YYYY
        'news.detik.com': lambda d: f"https://news.detik.com/indeks?date={d.strftime('%m/%d/%Y')}",
        'finance.detik.com': lambda d: f"https://finance.detik.com/indeks?date={d.strftime('%m/%d/%Y')}",
        'sport.detik.com': lambda d: f"https://sport.detik.com/indeks?date={d.strftime('%m/%d/%Y')}",
        'hot.detik.com': lambda d: f"https://hot.detik.com/indeks?date={d.strftime('%m/%d/%Y')}",
        'inet.detik.com': lambda d: f"https://inet.detik.com/indeks?date={d.strftime('%m/%d/%Y')}",
        'health.detik.com': lambda d: f"https://health.detik.com/indeks?date={d.strftime('%m/%d/%Y')}",

        # Kompas: indeks.kompas.com/?site=all&date=YYYY-MM-DD
        'kompas.com': lambda d: f"https://indeks.kompas.com/?site=all&date={d.strftime('%Y-%m-%d')}",
        'indeks.kompas.com': lambda d: f"https://indeks.kompas.com/?site=all&date={d.strftime('%Y-%m-%d')}",

        # Tempo: tempo.co/indeks/YYYY-MM-DD
        'tempo.co': lambda d: f"https://www.tempo.co/indeks/{d.strftime('%Y-%m-%d')}",

        # CNN Indonesia: cnnindonesia.com/indeks?date=YYYY/MM/DD
        'cnnindonesia.com': lambda d: f"https://www.cnnindonesia.com/indeks?date={d.strftime('%Y/%m/%d')}",

        # Liputan6
        'liputan6.com': lambda d: f"https://www.liputan6.com/indeks?q=&date={d.strftime('%Y-%m-%d')}",

        # Tribunnews
        'tribunnews.com': lambda d: f"https://www.tribunnews.com/index-news?date={d.strftime('%Y-%m-%d')}",

        # Antara
        'antaranews.com': lambda d: f"https://www.antaranews.com/indeks?tanggal={d.strftime('%Y-%m-%d')}",
    }

    # Cari pattern yang cocok
    url_builder = None
    for pattern_domain, builder in date_patterns.items():
        if pattern_domain in domain or domain.endswith(pattern_domain):
            url_builder = builder
            break

    if not url_builder:
        print(f"  ⚠ Situs {domain} belum punya pattern URL tanggal.")
        print(f"  → Menggunakan URL asli + filter tanggal setelah scrape.")
        return [base_url]

    # Generate URL untuk setiap tanggal dalam range
    urls = []
    current = start_date
    while current.date() <= end_date.date():
        urls.append(url_builder(current))
        current += timedelta(days=1)

    return urls

def setup_driver():
    
    import shutil

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    # Auto-detect browser yang tersedia
    browsers = [
        ('Google Chrome', ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable']),
        ('Brave', ['/usr/bin/brave-browser', '/usr/bin/brave-browser-stable']),
        ('Chromium', ['/usr/bin/chromium', '/usr/bin/chromium-browser']),
        ('Edge', ['/usr/bin/microsoft-edge', '/usr/bin/microsoft-edge-stable']),
    ]

    detected = None
    for name, paths in browsers:
        for path in paths:
            if shutil.which(path) or os.path.isfile(path):
                detected = (name, path)
                break
        if detected:
            break

    if detected:
        print(f"Browser terdeteksi: {detected[0]} ({detected[1]})")
        options.binary_location = detected[1]
    else:
        print("Tidak ada browser khusus terdeteksi, menggunakan default ChromeDriver.")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_article_links(driver, url, max_pages=3):
    """Temukan link artikel dari halaman index menggunakan Selenium + heuristik."""
    driver.get(url)
    time.sleep(3)


    parsed = urlparse(url)
    domain_parts = parsed.netloc.lower().replace('www.', '').split('.')
    if len(domain_parts) >= 2:
        root_domain = '.'.join(domain_parts[-2:])  # kompas.com, detik.com, dll
    else:
        root_domain = parsed.netloc.lower()

    # Keyword umum di URL artikel berita
    article_keywords = [
        '/read/', '/artikel/', '/berita/', '/news/',
        '/detail/', '/post/', '/story/', '/article/',
        '/opini/', '/nasional/', '/internasional/',
        '/hukum/', '/politik/', '/ekonomi/', '/olahraga/',
        '/sains/', '/digital/', '/gaya-hidup/', '/hiburan/',
        '/foto/', '/video/', '/cekfakta/', '/kolom/',
        '/tren/', '/global/', '/otomotif/', '/food/',
        '/hype/', '/badminton/', '/sepakbola/',
    ]

    # Path yang BUKAN artikel
    exclude_keywords = [
        '/tag/', '/kategori/', '/category/', '/author/',
        '/page/', '/search/', '/login/', '/register/',
        '/about/', '/contact/', '/privacy/', '/terms/',
        '#', 'javascript:', 'mailto:',
    ]

    article_links = set()
    pages_scraped = 0
    total_links_on_page = 0

    while pages_scraped < max_pages:
        elements = driver.find_elements(By.TAG_NAME, 'a')
        total_links_on_page = len(elements)

        for el in elements:
            href = el.get_attribute('href')
            if not href:
                continue

            # Cek root domain (fleksibel: subdomain boleh beda)
            href_domain = urlparse(href).netloc.lower().replace('www.', '')
            if root_domain not in href_domain:
                continue

            # Exclude non-article links
            if any(ex in href.lower() for ex in exclude_keywords):
                continue

            # Cek keyword di URL ATAU path cukup panjang (heuristik artikel)
            path = urlparse(href).path
            has_keyword = any(kw in href.lower() for kw in article_keywords)
            looks_like_article = len(path.split('/')) >= 3 and len(path) > 20

            if has_keyword or looks_like_article:
                article_links.add(href)

        pages_scraped += 1
        next_btn = None
        try:
            next_btn = driver.find_element(
                By.CSS_SELECTOR,
                'a.next, a[rel="next"], .pagination a.next, a.paging__link--next'
            )
        except Exception:
            pass

        if not next_btn:
            try:
                for el in driver.find_elements(By.TAG_NAME, 'a'):
                    text = el.text.strip()
                    if text in ('›', '»', 'Next', 'Selanjutnya'):
                        next_btn = el
                        break
            except Exception:
                pass

        if next_btn and pages_scraped < max_pages:
            try:
                next_btn.click()
                time.sleep(2)
            except Exception:
                break
        else:
            break

    print(f"Ditemukan {len(article_links)} link artikel (dari {total_links_on_page} link di halaman, domain: {root_domain}).")
    return list(article_links)


def scrape_article(driver, url):
    try:
        driver.get(url)
        time.sleep(1)

        hasil = extract_article_with_fallback(driver, url)

        if not hasil.get('title'):
            return None

        return hasil

    except Exception as e:
        print(f"  Gagal membuka {url}: {e}")
        return None


def main():
    url = input("Masukkan URL halaman berita: ").strip()
    if not url:
        print("URL tidak boleh kosong.")
        return

    # Filter tanggal (opsional)
    print("\n Filter tanggal (opsional, tekan Enter untuk skip):")
    print("   Format: YYYY-MM-DD | Shortcut: 'hari ini', 'kemarin'")

    start_date = None
    end_date = None

    inp_start = input("   Dari tanggal : ").strip()
    if inp_start:
        start_date = parse_input_date(inp_start)
        if not start_date:
            print("   Format tanggal tidak valid.")
            return

        inp_end = input("   Sampai tanggal (Enter = sama dengan dari): ").strip()
        if inp_end:
            end_date = parse_input_date(inp_end)
            if not end_date:
                print("   Format tanggal tidak valid.")
                return
        else:
            end_date = start_date  # Single date

        if start_date > end_date:
            start_date, end_date = end_date, start_date

        print(f"\n   Filter: {start_date.strftime('%Y-%m-%d')} s/d {end_date.strftime('%Y-%m-%d')}")
    else:
        print("   Tidak ada filter tanggal.")

    print("\nMemulai browser...")
    driver = setup_driver()

    try:
        if start_date and end_date:
            index_urls = build_date_urls(url, start_date, end_date)
            print(f"\n📋 {len(index_urls)} halaman indeks akan di-scrape:")
            for u in index_urls:
                print(f"   → {u}")
        else:
            index_urls = [url]

        # Cari link artikel dari semua halaman index
        article_links = []
        for idx_url in index_urls:
            print(f"\nMencari link artikel dari {idx_url}...")
            links = get_article_links(driver, idx_url)
            article_links.extend(links)

        # Hapus duplikat, pertahankan urutan
        seen = set()
        unique_links = []
        for link in article_links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)
        article_links = unique_links

        if not article_links:
            print("Tidak ditemukan link artikel.")
            return

        # Mulai dengan data kosong (reset setiap scrape)
        data_json = {"list": []}

        # Scrape setiap artikel
        berhasil = 0
        dilewati = 0
        print(f"\nMemproses {len(article_links)} artikel...\n")

        for i, link in enumerate(article_links, 1):
            print(f"[{i}/{len(article_links)}] {link}")
            hasil = scrape_article(driver, link)

            if not hasil:
                print(f"  ✗ Gagal mengekstrak data")
                continue

            # Filter tanggal jika aktif
            if start_date and end_date:
                if not article_matches_date(hasil, start_date, end_date):
                    dt = parse_date(hasil.get('date'))
                    dt_str = dt.strftime('%Y-%m-%d') if dt else '?'
                    print(f"  ⏭ Dilewati (tanggal: {dt_str})")
                    dilewati += 1
                    continue

            data_json["list"].append(hasil)
            berhasil += 1
            print(f"  ✓ {hasil['title'][:60]}")

        # Simpan hasil
        with open("data.json", "w") as file:
            json.dump(data_json, file, indent=4, ensure_ascii=False)

        print(f"\n=== Selesai ===")
        print(f"Berhasil: {berhasil}/{len(article_links)} artikel")
        if start_date:
            print(f"Dilewati (di luar tanggal): {dilewati} artikel")
        print(f"Data disimpan ke data.json")

    except Exception as e:
        print(f"\nTerjadi kesalahan: {e}")

    finally:
        driver.quit()
        print("Browser ditutup.")


if __name__ == '__main__':
    main()