from PyQt5.QtCore import QThread, pyqtSignal

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
        pass

    # Method untuk menghentikan proses scraping
    def stop(self):
        pass
