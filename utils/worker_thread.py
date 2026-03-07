from PyQt5.QtCore import QThread, pyqtSignal
from scraper.selenium_scraper import setup_driver, get_article_links, scrape_article, build_date_urls
from datetime import datetime

# Class ini berfungsi sebagai thread terpisah untuk menjalankan proses scraping berita
# agar tidak membuat GUI utama (main thread) menjadi freeze/not responding.
class ScraperWorker(QThread):
    article_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int, int)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str)  # Signal untuk mengirim log ke GUI

    # Inisialisasi class dengan parameter yang dibutuhkan untuk scraping
    def __init__(self, url, limit=0, start_date=None, end_date=None, headless=True, parent=None):
        super().__init__(parent)
        self.url = url
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self.headless = headless  # Menyimpan preferensi headless mode
        self._running = True

    # Method utama yang akan dijalankan saat thread dimulai
    def run(self):
        driver = None
        try:
            driver = setup_driver(headless=self.headless)  # Gunakan parameter headless dari user
            self.log_message.emit('[INFO]  Browser berhasil dijalankan.')

            # Jika ada filter tanggal, gunakan build_date_urls untuk semua halaman indeks
            if self.start_date and self.end_date:
                start_dt = datetime.combine(self.start_date, datetime.min.time())
                end_dt = datetime.combine(self.end_date, datetime.min.time())
                index_urls = build_date_urls(self.url, start_dt, end_dt)
                self.log_message.emit(f'[INFO]  Filter tanggal aktif: {self.start_date} s/d {self.end_date}')
                self.log_message.emit(f'[INFO]  {len(index_urls)} halaman indeks akan di-scrape.')
            else:
                index_urls = [self.url]

            # Kumpulkan link artikel dari semua halaman indeks
            all_links = []
            seen = set()  # Track duplikat sejak awal agar limit akurat
            for idx_url in index_urls:
                if not self._running:
                    break
                self.log_message.emit(f'[INFO]  Mencari link artikel dari {idx_url}...')
                links = get_article_links(driver, idx_url)
                # Tambahkan hanya link unik
                for link in links:
                    if link not in seen:
                        seen.add(link)
                        all_links.append(link)
                self.log_message.emit(f'[INFO]  Ditemukan {len(links)} link dari halaman tersebut (total unik: {len(all_links)}).')
                # Hentikan pencarian jika sudah cukup untuk limit
                if self.limit > 0 and len(all_links) >= self.limit:
                    self.log_message.emit(f'[INFO]  Limit {self.limit} tercapai, menghentikan pencarian link.')
                    break

            # Hapus duplikat, pertahankan urutan
            seen = set()
            unique_links = []
            for link in all_links:
                if link not in seen:
                    seen.add(link)
                    unique_links.append(link)
            all_links = unique_links

            self.log_message.emit(f'[INFO]  Total {len(all_links)} link artikel unik ditemukan.')

            # Terapkan limit jika ada
            if self.limit > 0:
                all_links = all_links[:self.limit]
                self.log_message.emit(f'[INFO]  Limit aktif: memproses {len(all_links)} artikel.')

            total = len(all_links)

            if total == 0:
                self.log_message.emit('[WARN]  Tidak ditemukan link artikel.')
                return

            # Scrape setiap artikel
            for i, link in enumerate(all_links):
                if not self._running:
                    break
                article = scrape_article(driver, link)
                if article is not None:
                    self.article_ready.emit(article)
                else:
                    self.log_message.emit(f'[WARN]  Gagal mengekstrak: {link[:80]}')
                self.progress_update.emit(i + 1, total)
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            if driver:
                try:
                    driver.quit()
                    self.log_message.emit('[INFO]  Browser ditutup.')
                except Exception:
                    pass
            self.finished.emit()

    def stop(self):
        self._running = False # Menghentikan proses scraping

