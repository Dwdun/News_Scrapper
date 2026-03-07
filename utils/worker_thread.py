from PyQt5.QtCore import QThread, pyqtSignal
from scraper.selenium_scraper import setup_driver, get_article_links, scrape_article

# Class ini berfungsi sebagai thread terpisah untuk menjalankan proses scraping berita
# agar tidak membuat GUI utama (main thread) menjadi freeze/not responding.
class ScraperWorker(QThread):
    article_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(int, int)
    finished = pyqtSignal()
    error_occurred = pyqtSignal(str)

    # Inisialisasi class dengan parameter yang dibutuhkan untuk scraping
    def __init__(self, url, limit=0, start_date=None, end_date=None, parent=None):
        super().__init__(parent)
        self.url = url
        self.limit = limit
        self.start_date = start_date
        self.end_date = end_date
        self._running = True

    # Method utama yang akan dijalankan saat thread dimulai
    def run(self):
        try:
            driver = setup_driver()
            links = get_article_links(driver, self.url) # Panggil fungsi get_article_links
            if self.limit > 0: # Cek jika ada batas limit
                links = links[:self.limit] # Potong list sesuai limit
            total = len(links) # Simpan panjang list

            for i, link in enumerate(links): # Loop setiap link artikel
                article = scrape_article(driver, link) # Scraping artikel
                if article is not None: # Jika artikel berhasil di-scrape
                    self.article_ready.emit(article) # Emit signal article_ready
                self.progress_update.emit(i + 1, total) # Emit progress setiap iterasi
                if not self._running: break # Hentikan loop jika thread dibatalkan
        except Exception as e:
            self.error_occurred.emit(str(e))
        finally:
            self.finished.emit()

    def stop(self):
        self._running = False # Menghentikan proses scraping

