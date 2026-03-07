import sys
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QSpinBox, QDateEdit, QCheckBox, QTextEdit, QFileDialog, QApplication
)
from PyQt5.QtCore import QDate, Qt
from utils.worker_thread import ScraperWorker
from utils.date_filter import filter_by_date
from utils.exporter import export_to_csv, export_to_excel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Mewscrapper © A1 Pokemoon')
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

        # === PROGRESS BAR & LABEL STATUS ===
        r3 = QVBoxLayout()
        r3.setSpacing(4)

        self.prog_lbl = QLabel('Siap — Masukkan URL dan klik Start.')
        self.prog_lbl.setStyleSheet("""
            color: #555555;
            font-size: 12px;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        """)

        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(6)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet("""
            QProgressBar {
                background-color: #1a1a1a;
                border: none;
                border-radius: 3px;
            }
            QProgressBar::chunk {
                background-color: #e8e8e8;
                border-radius: 3px;
            }
        """)

        r3.addWidget(self.prog_lbl)
        r3.addWidget(self.progress)
        lay.addLayout(r3)
        
        # === TABEL 5 KOLOM ===
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            'No', 'Judul', 'Tanggal', 'Isi (preview)', 'URL'
        ])

        # Lebar kolom
        self.table.setColumnWidth(0, 50)   # No
        self.table.setColumnWidth(1, 280)  # Judul
        self.table.setColumnWidth(2, 110)  # Tanggal
        self.table.setColumnWidth(3, 350)  # Isi preview
        self.table.horizontalHeader().setStretchLastSection(True)  # URL isi sisa

        # Tinggi baris
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)  # sembunyikan nomor baris kiri

        # Behaviour
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # tidak bisa diedit
        self.table.setSelectionBehavior(QTableWidget.SelectRows)  # pilih per baris
        self.table.setAlternatingRowColors(True)  # warna selang-seling
        self.table.setShowGrid(False)  # sembunyikan garis grid

        self.table.setStyleSheet("""
            QTableWidget {
                background-color: #0f0f0f;
                border: 1px solid #1e1e1e;
                border-radius: 8px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 13px;
                outline: none;
            }
            QTableWidget::item {
                padding: 8px 12px;
                color: #e8e8e8;
                border-bottom: 1px solid #1a1a1a;
            }
            QTableWidget::item:selected {
                background-color: #1e1e1e;
                color: #ffffff;
            }
            QTableWidget::item:alternate {
                background-color: #0a0a0a;
            }
            QHeaderView::section {
                background-color: #0f0f0f;
                color: #444444;
                padding: 10px 12px;
                border: none;
                border-bottom: 1px solid #1e1e1e;
                font-weight: 600;
                font-size: 11px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
        """)

        lay.addWidget(self.table, stretch=1)
        
        # === TOMBOL EXPORT ===
        r4 = QHBoxLayout()
        r4.setSpacing(8)

        self.btn_csv = QPushButton('⬇  Export CSV')
        self.btn_csv.setFixedHeight(40)
        self.btn_csv.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #888888;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                padding: 8px 18px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                border-color: #e8e8e8;
                color: #e8e8e8;
            }
            QPushButton:disabled { color: #2a2a2a; border-color: #1e1e1e; }
        """)

        self.btn_excel = QPushButton('⬇  Export Excel')
        self.btn_excel.setFixedHeight(40)
        self.btn_excel.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                color: #888888;
                border: 1px solid #2a2a2a;
                border-radius: 6px;
                padding: 8px 18px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 13px;
                font-weight: 500;
            }
            QPushButton:hover {
                border-color: #4ade80;
                color: #4ade80;
            }
            QPushButton:disabled { color: #2a2a2a; border-color: #1e1e1e; }
        """)

        # Label jumlah artikel
        self.lbl_count = QLabel('0 artikel')
        self.lbl_count.setStyleSheet("""
            color: #333333;
            font-size: 12px;
            font-family: 'Inter', 'Segoe UI', sans-serif;
        """)

        r4.addWidget(self.lbl_count)       # kiri — jumlah artikel
        r4.addStretch()                    # dorong tombol ke kanan
        r4.addWidget(self.btn_csv)
        r4.addWidget(self.btn_excel)
        lay.addLayout(r4)
        
        # === PANEL LOG ===
        # Header log
        r5 = QHBoxLayout()

        lbl_log = QLabel('LOG')
        lbl_log.setStyleSheet("""
            color: #333333;
            font-size: 10px;
            font-weight: 700;
            font-family: 'Inter', 'Segoe UI', sans-serif;
            letter-spacing: 1px;
        """)

        self.btn_clear_log = QPushButton('Hapus Log')
        self.btn_clear_log.setFixedHeight(24)
        self.btn_clear_log.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2a2a2a;
                border: 1px solid #1e1e1e;
                border-radius: 4px;
                padding: 0px 10px;
                font-family: 'Inter', 'Segoe UI', sans-serif;
                font-size: 10px;
            }
            QPushButton:hover {
                color: #555555;
                border-color: #333333;
            }
        """)

        r5.addWidget(lbl_log)
        r5.addStretch()
        r5.addWidget(self.btn_clear_log)
        lay.addLayout(r5)

        # Log box
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        self.log_box.setFixedHeight(120)
        self.log_box.setStyleSheet("""
            QTextEdit {
                background-color: #0a0a0a;
                border: 1px solid #1a1a1a;
                border-radius: 8px;
                color: #4ade80;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 11px;
                padding: 8px;
            }
        """)

        lay.addWidget(self.log_box)

        # Connect tombol hapus log
        self.btn_clear_log.clicked.connect(self.log_box.clear)
        
        # === CONNECT SEMUA TOMBOL ===
        self.btn_start.clicked.connect(self.start_scraping)
        self.btn_stop.clicked.connect(self.stop_scraping)
        self.btn_csv.clicked.connect(self.do_export_csv)
        self.btn_excel.clicked.connect(self.do_export_excel)
        
    # =============================
    # SLOT FUNCTIONS
    # =============================

    def start_scraping(self):
        url = self.url_in.text().strip()

        # Validasi URL tidak kosong
        if not url:
            self.log_box.append('[WARN]  Masukkan URL dulu sebelum klik Start!')
            return

        # Reset tabel dan artikel
        self.articles = []
        self.table.setRowCount(0)
        self.lbl_count.setText('0 artikel')
        self.lbl_count.setStyleSheet('color: #333333; font-size: 12px;')
        self.log_box.clear()
        self.progress.setValue(0)

        # Ambil parameter filter
        sd = self.dt_start.date().toPyDate() if self.chk_date.isChecked() else None
        ed = self.dt_end.date().toPyDate() if self.chk_date.isChecked() else None
         
        self.worker = ScraperWorker(url, self.spin_lim.value(), sd, ed)
        self.worker.article_ready.connect(self.on_article)
        self.worker.progress_update.connect(self.on_progress)
        self.worker.finished.connect(self.on_done)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.start()

        # Toggle tombol
        self.btn_start.setEnabled(False)
        self.btn_stop.setEnabled(True)
        self.prog_lbl.setText('Menghubungkan ke URL...')
        self.log_box.append(f'[INFO]  Scraping dimulai: {url}')

    def stop_scraping(self):
        if self.worker:
            self.worker.stop()
        self.log_box.append('[INFO]  Scraping dihentikan oleh user.')

    def on_article(self, article: dict):
        # Filter tanggal kalau aktif
        if self.chk_date.isChecked():
            hasil = filter_by_date(
                [article],
                self.dt_start.date().toPyDate(),
                self.dt_end.date().toPyDate()
            )
            if not hasil:
                return  # artikel tidak lolos filter, skip

        # Tambah ke list
        self.articles.append(article)

        # Tambah baris baru ke tabel
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(str(row + 1)))
        self.table.setItem(row, 1, QTableWidgetItem(article.get('title', '')))
        self.table.setItem(row, 2, QTableWidgetItem(article.get('date', '')))
        self.table.setItem(row, 3, QTableWidgetItem(article.get('content', '')[:80] + '...'))
        self.table.setItem(row, 4, QTableWidgetItem(article.get('url', '')))
        self.table.scrollToBottom()

        # Update label count
        self.lbl_count.setText(f'{len(self.articles)} artikel')
        self.log_box.append(f'[INFO]  ✓ Artikel {row + 1}: {article.get("title", "")[:50]}...')

    def on_progress(self, current: int, total: int):
        self.progress.setMaximum(total)
        self.progress.setValue(current)
        self.prog_lbl.setText(f'Memproses {current}/{total} artikel...')

    def on_done(self):
        # Reset tombol
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

        # Update label dan log
        total = len(self.articles)
        self.prog_lbl.setText(f'Selesai — {total} artikel berhasil.')
        self.lbl_count.setText(f'{total} artikel')
        self.lbl_count.setStyleSheet('color: #4ade80; font-size: 12px;')
        self.log_box.append(f'[DONE]  Scraping selesai — {total} artikel berhasil.')

    def on_error(self, msg: str):
        self.log_box.append(f'[ERROR]  {msg}')
        self.btn_start.setEnabled(True)
        self.btn_stop.setEnabled(False)

    def do_export_csv(self):
        if not self.articles:
            self.log_box.append('[WARN]  Tidak ada artikel untuk diekspor!')
            return
        path, _ = QFileDialog.getSaveFileName(
            self, 'Simpan CSV', 'hasil_scraping.csv', 'CSV (*.csv)'
        )
        if path:
            export_to_csv(self.articles, path)
            self.log_box.append(f'[DONE]  CSV tersimpan: {path}')

    def do_export_excel(self):
        if not self.articles:
            self.log_box.append('[WARN]  Tidak ada artikel untuk diekspor!')
            return
        path, _ = QFileDialog.getSaveFileName(
            self, 'Simpan Excel', 'hasil_scraping.xlsx', 'Excel (*.xlsx)'
        )
        if path:
            export_to_excel(self.articles, path)
            self.log_box.append(f'[DONE]  Excel tersimpan: {path}')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())