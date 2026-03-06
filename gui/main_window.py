import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QSpinBox, QDateEdit, QCheckBox, QTextEdit, QFileDialog, QApplication
)
from PyQt5.QtCore import QDate, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('MewScrapper © A1 Pokemoon')
        self.setMinimumSize(1200, 750)
        self.articles = []   # list artikel hasil scraping
        self.worker = None   # akan diisi ScraperWorker nanti
        self._init_ui()
        
    def _init_ui(self):
        # === Warna & Syle ===
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0f0f0f;
                color: #e8e8e8;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QLineEdit {
                background-color: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                padding: 8px 12px;
                color: #e8e8e8;
            }
            QLineEdit:focus {
                border: 1px solid #555555;
            }
            QTableWidget {
                background-color: #111111;
                border: 1px solid #1e1e1e;
                border-radius: 6px;
                gridline-color: #1e1e1e;
            }
            QTableWidget::item {
                padding: 6px;
                border-bottom: 1px solid #1e1e1e;
            }
            QTableWidget::item:selected {
                background-color: #2a2a2a;
            }
            QHeaderView::section {
                background-color: #1a1a1a;
                color: #888888;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #2a2a2a;
                font-weight: bold;
                font-size: 11px;
                text-transform: uppercase;
            }
            QProgressBar {
                background-color: #1a1a1a;
                border: none;
                border-radius: 4px;
                height: 6px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #e8e8e8;
                border-radius: 4px;
            }
            QTextEdit {
                background-color: #0a0a0a;
                border: 1px solid #1e1e1e;
                border-radius: 6px;
                color: #4ade80;
                font-family: 'Consolas', monospace;
                font-size: 11px;
            }
            QCheckBox { color: #888888; }
            QCheckBox:checked { color: #e8e8e8; }
            QDateEdit, QSpinBox {
                background-color: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                padding: 6px 10px;
                color: #e8e8e8;
            }
            QLabel { color: #888888; }
        """)

        # === Layout Utama ===
        root = QWidget()
        self.setCentralWidget(root)
        lay = QVBoxLayout(root)
        lay.setSpacing(6)
        lay.setContentsMargins(20, 20, 20, 20)
        
        # === Bar Input URL ===
        r1 = QHBoxLayout()  

        self.url_in = QLineEdit()
        self.url_in.setPlaceholderText('Masukkan URL halaman berita...')
        self.url_in.setFixedHeight(48)       
        self.url_in.setMaximumWidth(800)     
        self.url_in.setStyleSheet("""
            QLineEdit {
                background-color: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 8px 16px;
                color: #e8e8e8;
                font-size: 20px;
            }
            QLineEdit:focus { border: 1px solid #555555; }
        """)

        self.btn_start = QPushButton('▶  Start')
        self.btn_start.setFixedHeight(48)    
        self.btn_start.setFixedWidth(120)
        self.btn_start.setStyleSheet("""
            QPushButton {
                background-color: #e8e8e8;
                color: #0f0f0f;
                border: none;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover { background-color: #16a34a; }
            QPushButton:disabled { background-color: #2a2a2a; color: #555555; }
        """)

        self.btn_stop = QPushButton('■  Stop')
        self.btn_stop.setFixedHeight(48)     
        self.btn_stop.setFixedWidth(120)
        self.btn_stop.setEnabled(False)
        self.btn_stop.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #ff4444;
                border: 1px solid #2a2a2a;
                border-radius: 8px;
                padding: 8px 20px;
                font-weight: bold;
                font-size: 20px;
            }
            QPushButton:hover { background-color: #dc2626; color: #fff; }
            QPushButton:disabled { color: #333333; border-color: #1e1e1e; }
        """)

        url_label = QLabel('URL :')
        url_label.setStyleSheet("color: #888888; font-size: 18px;")

        r1.addStretch()                          
        r1.addWidget(url_label)
        r1.addWidget(self.url_in)
        r1.addWidget(self.btn_start)
        r1.addWidget(self.btn_stop)
        r1.addStretch()                        
        lay.addLayout(r1)
        
        # === Filter dan Limit ===
        r2 = QHBoxLayout()
        r2.setSpacing(10)

        self.chk_date = QCheckBox('Filter Tanggal')
        self.chk_date.setStyleSheet("""
            QCheckBox {
                color: #888888;
                font-size: 13px;
            }
            QCheckBox:checked { color: #e8e8e8; }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
                border: 1px solid #2a2a2a;
                border-radius: 4px;
                background-color: #1a1a1a;
            }
            QCheckBox::indicator:checked {
                background-color: #e8e8e8;
            }
        """)

        self.dt_start = QDateEdit(QDate.currentDate())
        self.dt_start.setCalendarPopup(True)
        self.dt_start.setFixedHeight(44)
        self.dt_start.setEnabled(False)  # nonaktif dulu sebelum checkbox dicentang

        self.dt_end = QDateEdit(QDate.currentDate())
        self.dt_end.setCalendarPopup(True)
        self.dt_end.setFixedHeight(44)
        self.dt_end.setEnabled(False)  # nonaktif dulu sebelum checkbox dicentang

        self.spin_lim = QSpinBox()
        self.spin_lim.setMinimum(0)
        self.spin_lim.setMaximum(9999)
        self.spin_lim.setValue(0)
        self.spin_lim.setPrefix('Limit : ')
        self.spin_lim.setSuffix('  (0 = semua)')
        self.spin_lim.setFixedHeight(44)
        self.spin_lim.setStyleSheet("""
            QSpinBox {
                background-color: #1a1a1a;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                padding: 6px 10px;
                color: #e8e8e8;
                font-size: 13px;
            }
        """)

        lbl_dari = QLabel('Dari :')
        lbl_dari.setStyleSheet("color: #888888; font-size: 14px;")
        lbl_sd = QLabel('s/d :')
        lbl_sd.setStyleSheet("color: #888888; font-size: 14px;")

        r2.addStretch()
        r2.addWidget(self.chk_date)
        r2.addSpacing(10)
        r2.addWidget(lbl_dari)
        r2.addWidget(self.dt_start)
        r2.addWidget(lbl_sd)
        r2.addWidget(self.dt_end)
        r2.addSpacing(20)
        r2.addWidget(self.spin_lim)
        r2.addStretch()
        lay.addLayout(r2)

        # Checkbox mengaktifkan/nonaktifkan DateEdit
        self.chk_date.toggled.connect(self.dt_start.setEnabled)
        self.chk_date.toggled.connect(self.dt_end.setEnabled)

        # === Status Label + Progress Bar ===
        # QLabel untuk menampilkan teks status scraping secara deskriptif.
        # Diletakkan di atas progress bar agar user tahu apa yang sedang terjadi
        # sebelum melihat angka persentase.
        self.lbl_status = QLabel('Idle')
        self.lbl_status.setAlignment(Qt.AlignCenter)   # teks selalu di tengah
        self.lbl_status.setStyleSheet("""
            QLabel {
                color: #888888;          /* abu-abu sekunder — netral saat Idle */
                font-size: 13px;
                padding: 4px 0px;
            }
        """)

        # QProgressBar menampilkan kemajuan scraping secara visual.
        # setRange(0, 0) → mode "indeterminate" (animasi berputar) saat total belum diketahui.
        # setRange(0, N) → mode normal 0–N setelah total artikel diketahui.
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)       # indeterminate dulu, berubah saat scraping mulai
        self.progress_bar.setValue(0)
        self.progress_bar.setFixedHeight(6)    # tipis seperti garis — mengikuti design system
        self.progress_bar.setTextVisible(False)  # teks % disembunyikan; kita pakai lbl_status
        # Style khusus progress bar agar tidak dioverride global stylesheet
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1a1a1a;   /* card color */
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #e8e8e8;   /* putih — konsisten dengan btn_start */
                border-radius: 3px;
            }
        """)

        lay.addWidget(self.lbl_status)
        lay.addWidget(self.progress_bar)
        
    # ------------------------------------------------------------------
    # SLOT: on_progress
    # Dipanggil oleh sinyal  ScraperWorker.progress_update(current, total)
    # yang dikirim Faqih dari worker_thread.py setiap kali satu artikel
    # selesai di-scrape.
    #
    # Parameter:
    #   current (int) — nomor artikel yang baru selesai (1-based)
    #   total   (int) — total artikel yang akan di-scrape
    # ------------------------------------------------------------------
    def on_progress(self, current: int, total: int):
        # Pertama kali total diketahui → set range agar bar tidak lagi "indeterminate"
        if self.progress_bar.maximum() != total:
            self.progress_bar.setRange(0, total)

        self.progress_bar.setValue(current)

        # Update label dengan teks berwarna putih (aktif) saat scraping berjalan
        self.lbl_status.setText(f'Scraping artikel {current} / {total}…')
        self.lbl_status.setStyleSheet("""
            QLabel {
                color: #e8e8e8;   /* teks utama — menandakan proses aktif */
                font-size: 13px;
                padding: 4px 0px;
            }
        """)

    # ------------------------------------------------------------------
    # SLOT: on_status
    # Slot utilitas untuk memperbarui HANYA teks label tanpa menyentuh bar.
    # Berguna untuk pesan dari sinyal finished() atau error_occurred(str)
    # milik Faqih.
    #
    # Parameter:
    #   message (str)  — teks yang akan ditampilkan
    #   is_error (bool) — jika True teks jadi merah, default False
    # ------------------------------------------------------------------
    def on_status(self, message: str, is_error: bool = False):
        self.lbl_status.setText(message)
        text_color = '#ff4444' if is_error else '#888888'   # merah saat error, abu saat normal
        self.lbl_status.setStyleSheet(f"""
            QLabel {{
                color: {text_color};
                font-size: 13px;
                padding: 4px 0px;
            }}
        """)

        # Jika bukan error dan bar sudah di titik akhir → reset ke 0 agar bersih
        if not is_error and self.progress_bar.value() == self.progress_bar.maximum():
            self.progress_bar.setRange(0, 0)   # kembali ke indeterminate (kosong)
            self.progress_bar.setValue(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())