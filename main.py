import sys # Import sys untuk penanganan argumen baris perintah
from PyQt5.QtWidgets import QApplication # Import QApplication untuk aplikasi GUI
from gui.main_window import MainWindow # Import MainWindow untuk tampilan utama

if __name__ == '__main__': # Titik awal eksekusi program utama
    app = QApplication(sys.argv) # Inisialisasi aplikasi GUI
    app.setApplicationName("News Scraper") # Set nama aplikasi menjadi "News Scraper"
    window = MainWindow() # Buat instance dari MainWindow
    window.show() # Tampilkan MainWindow
    sys.exit(app.exec_()) # Mulai event loop aplikasi dan eksekusi keluar saat loop selesai
