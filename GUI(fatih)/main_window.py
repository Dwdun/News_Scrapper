from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QProgressBar, QSpinBox, QDateEdit, QCheckBox, QTextEdit, QFileDialog
)
from PyQt5.QtCore import QDate

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Newscrapper © A1 Pokemoon')
        self.setMinimumSize(1200, 750)
        self.articles = []   # list artikel hasil scraping
        self.worker = None   # akan diisi ScraperWorker nanti
        self._init_ui()
        
    def _init_ui(self):
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

        root = QWidget()
        self.setCentralWidget(root)
        lay = QVBoxLayout(root)
        lay.setSpacing(10)
        lay.setContentsMargins(20, 20, 20, 20)