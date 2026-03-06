from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, urljoin
import json
import os
import time


def setup_driver():
    import shutil
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

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
    driver.get(url)
    time.sleep(3)

    parsed = urlparse(url)
    domain_parts = parsed.netloc.lower().replace('www.', '').split('.')
    if len(domain_parts) >= 2:
        root_domain = '.'.join(domain_parts[-2:])
    else:
        root_domain = parsed.netloc.lower()

    article_keywords = [
        '/read/', '/artikel/', '/berita/', '/news/',
        '/detail/', '/post/', '/story/', '/article/',
        '/opini/', '/nasional/', '/internasional/',
    ]

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

            href_domain = urlparse(href).netloc.lower().replace('www.', '')
            if root_domain not in href_domain:
                continue

            if any(ex in href.lower() for ex in exclude_keywords):
                continue

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


if __name__ == '__main__':
    driver = setup_driver()
    print("Browser berhasil dijalankan!")
    driver.quit()
