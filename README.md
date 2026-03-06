# 📰 NewsPedia — Aplikasi Scraping Berita Otomatis

> Aplikasi desktop Python untuk mengumpulkan artikel berita secara otomatis dari berbagai website berita Indonesia menggunakan Selenium dan PyQt5.

---

## 👥 Tim Pengembang

| Nama | Peran | File |
|---|---|---|
| **Faqih** | Threading & Integrasi (Lead) | `main.py`, `utils/worker_thread.py` |
| **Bima** | Selenium Scraper | `scraper/selenium_scraper.py`, `scraper/article_extractor.py` |
| **Fatih** | GUI Developer (PyQt5) | `gui/main_window.py`, `gui/dialogs.py` |
| **Anin** | Export & Filter Tanggal | `utils/exporter.py`, `utils/date_filter.py` |
| **Irfan** | Logging & Laporan PDF | `utils/logger.py`, `docs/laporan.pdf` |

---

## 📋 Deskripsi Aplikasi

NewsHarvest adalah aplikasi desktop berbasis Python yang memungkinkan pengguna mengumpulkan artikel berita secara otomatis dari berbagai website berita. Pengguna cukup memasukkan satu URL halaman berita, kemudian sistem secara otomatis:

1. Mengumpulkan semua link artikel di halaman tersebut
2. Membuka setiap artikel satu per satu menggunakan Chrome headless
3. Mengekstraksi judul, tanggal, dan isi berita
4. Menampilkan hasil secara real-time di antarmuka GUI
5. Menyimpan hasil ke format CSV atau Excel

Proses scraping berjalan di background thread sehingga GUI tidak freeze selama proses berlangsung.

---

## ✨ Fitur Utama

- **Scraping otomatis** — input URL, klik Start, semua artikel dikumpulkan otomatis
- **Real-time display** — artikel muncul satu per satu saat berhasil di-scrape
- **Multi-website** — mendukung berbagai website berita Indonesia (CNN Indonesia, Detik, Kompas, Tribun, dll)
- **Filter tanggal** — saring artikel berdasarkan rentang tanggal tertentu
- **Limit artikel** — batasi jumlah artikel yang ingin dikumpulkan
- **Export CSV & Excel** — simpan hasil scraping ke file
- **Tombol Stop** — hentikan proses scraping kapan saja
- **Panel log** — pantau aktivitas scraping secara real-time
- **Headless mode** — Chrome berjalan di background tanpa muncul di layar

---

## 🛠️ Teknologi yang Digunakan

| Library | Versi | Fungsi |
|---|---|---|
| `selenium` | >=4.0.0 | Otomatisasi browser Chrome |
| `webdriver-manager` | >=4.0.0 | Auto-download ChromeDriver |
| `PyQt5` | >=5.15.0 | Framework GUI |
| `openpyxl` | >=3.1.0 | Export ke Excel (.xlsx) |
| `dateparser` | >=1.1.0 | Parse format tanggal berbagai bahasa |
| `beautifulsoup4` | >=4.12.0 | Parsing HTML helper |

---

## 📁 Struktur Project

```
news-scraper/
├── main.py                      # Entry point aplikasi
├── requirements.txt             # Daftar library yang dibutuhkan
├── README.md                    # Dokumentasi project
├── .gitignore                   # File yang diabaikan Git
│
├── scraper/                     # Modul scraping (Bima)
│   ├── __init__.py
│   ├── selenium_scraper.py      # Fungsi utama scraping
│   └── article_extractor.py    # Helper ekstraksi konten
│
├── gui/                         # Modul GUI (Fatih)
│   ├── __init__.py
│   ├── main_window.py           # Jendela utama aplikasi
│   └── dialogs.py               # Dialog konfirmasi
│
├── utils/                       # Modul utilitas
│   ├── __init__.py
│   ├── worker_thread.py         # Threading scraping (Faqih)
│   ├── exporter.py              # Export CSV & Excel (Anin)
│   ├── date_filter.py           # Filter tanggal (Anin)
│   └── logger.py                # Logging sistem (Irfan)
│
├── docs/                        # Dokumentasi
│   ├── laporan.pdf              # Laporan teknis (Irfan)
│   └── screenshots/             # Screenshot aplikasi (Fatih)
│
├── logs/                        # File log (auto-generated)
│   └── app.log
│
└── output/                      # Hasil export (auto-generated)
```

---

## ⚙️ Instalasi

### Prasyarat
- Python 3.8 atau lebih baru
- Google Chrome (versi terbaru)
- Git

### Langkah Instalasi

**1. Clone repository**
```bash
git clone https://github.com/[username]/news-scraper.git
cd news-scraper
```

**2. Install semua library**
```bash
pip install -r requirements.txt
```

Atau install manual:
```bash
pip install selenium webdriver-manager PyQt5 openpyxl dateparser beautifulsoup4
```

**3. Jalankan aplikasi**
```bash
python main.py
```

---

## 🚀 Panduan Penggunaan

### Scraping Artikel

1. Buka aplikasi dengan `python main.py`
2. Masukkan URL halaman berita di kolom input, contoh:
   ```
   https://www.cnnindonesia.com/nasional
   ```
3. Atur pengaturan opsional:
   - **Limit artikel** — centang dan isi angka jika ingin membatasi jumlah artikel
   - **Filter tanggal** — centang dan pilih rentang tanggal
   - **Headless mode** — centang agar Chrome tidak muncul di layar
4. Klik tombol **▶ Start** untuk memulai
5. Artikel akan muncul satu per satu di tabel secara real-time
6. Klik **■ Stop** kapan saja untuk menghentikan proses

### Export Data

1. Tunggu hingga scraping selesai atau klik Stop
2. Klik **Export CSV** untuk menyimpan ke format `.csv`
3. Klik **Export Excel** untuk menyimpan ke format `.xlsx`
4. Pilih lokasi penyimpanan di dialog yang muncul

### Filter Tanggal

1. Centang checkbox **Filter Tanggal**
2. Pilih tanggal mulai dan tanggal akhir
3. Hanya artikel dalam rentang tanggal tersebut yang akan ditampilkan
4. Klik Start untuk mulai scraping dengan filter aktif

---

## 🌐 Website yang Didukung

Aplikasi ini menggunakan multiple fallback CSS selector sehingga dapat bekerja di berbagai website berita. Website yang direkomendasikan:

| Website | URL | Status |
|---|---|---|
| CNN Indonesia | cnnindonesia.com | ✅ Direkomendasikan |
| Detik | detik.com | ✅ Direkomendasikan |
| Kompas | kompas.com | ✅ Direkomendasikan |
| Tribun News | tribunnews.com | ✅ Direkomendasikan |
| Tempo | tempo.co | ⚠️ Mungkin lebih lambat |
| Republika | republika.co.id | ⚠️ Struktur kompleks |

> **Catatan:** Website yang memerlukan login atau menggunakan proteksi anti-bot (Cloudflare) tidak dapat di-scrape.

---

## 📝 Format Data Hasil Scraping

Setiap artikel yang berhasil di-scrape akan memiliki format berikut:

| Kolom | Tipe | Deskripsi |
|---|---|---|
| `No` | int | Nomor urut artikel |
| `Judul` | str | Judul artikel berita |
| `Tanggal` | str | Tanggal publikasi artikel |
| `Isi` | str | Isi/konten artikel (maks. 600 karakter) |
| `URL` | str | Link langsung ke artikel |

---

## 🔧 Konfigurasi

### Headless Mode
Untuk melihat proses scraping di browser (berguna saat debugging):
- Di GUI: hilangkan centang pada checkbox **Headless mode**
- Di kode (`scraper/selenium_scraper.py`): hapus atau comment baris `options.add_argument('--headless')`

### Mengubah Batas Konten Artikel
Di file `scraper/article_extractor.py`, ubah nilai `600` pada baris:
```python
return content[:600]  # ubah angka ini sesuai kebutuhan
```

---

## 🐛 Troubleshooting

### Chrome tidak ditemukan
```
WebDriverException: Chrome not found
```
**Solusi:** Install Google Chrome dari [chrome.google.com](https://chrome.google.com)

### ChromeDriver versi tidak cocok
```
SessionNotCreatedException: Chrome version mismatch
```
**Solusi:** Library `webdriver-manager` akan otomatis download ChromeDriver yang sesuai. Pastikan koneksi internet aktif saat pertama kali menjalankan.

### Artikel tidak berhasil di-scrape
```
Artikel: 0 dari X berhasil
```
**Solusi:**
- Coba matikan headless mode untuk melihat apa yang terjadi di browser
- Cek apakah website memerlukan login
- Coba tambah delay dengan mengedit `time.sleep()` di `selenium_scraper.py`

### PyQt5 tidak terinstall
```
ModuleNotFoundError: No module named 'PyQt5'
```
**Solusi:**
```bash
pip install PyQt5
```

### File log tidak terbuat
Folder `logs/` akan dibuat otomatis saat pertama kali menjalankan aplikasi. Jika tidak terbuat, pastikan kamu punya permission menulis di folder project.

---

## 📊 Alur Kerja Aplikasi

```
User input URL
      ↓
ScraperWorker.start() — berjalan di background thread
      ↓
setup_driver() — inisialisasi Chrome headless
      ↓
get_article_links() — kumpulkan semua URL artikel
      ↓
Loop setiap URL:
  scrape_article() — ekstraksi judul/tanggal/isi
  emit article_ready → tampil di GUI
  emit progress_update → update progress bar
      ↓
emit finished() — scraping selesai
      ↓
User klik Export → simpan ke CSV/Excel
```

---

## 🤝 Kontribusi (Untuk Anggota Tim)

### Workflow Git

```bash
# Sebelum mulai coding
git pull origin main

# Setelah selesai 1 fitur
git add .
git commit -m "feat: deskripsi singkat"
git push origin [nama-branch-kamu]
```

### Format Pesan Commit

| Prefix | Dipakai untuk |
|---|---|
| `feat:` | Menambah fitur baru |
| `fix:` | Memperbaiki bug |
| `style:` | Perubahan tampilan |
| `docs:` | Perubahan dokumentasi |
| `test:` | Menambah testing |
| `refactor:` | Perbaiki kode tanpa ubah fungsi |

### Branch per Anggota

| Branch | Penanggung Jawab |
|---|---|
| `feature/faqih-threading` | Faqih |
| `feature/bima-scraper` | Bima |
| `feature/fatih-gui` | Fatih |
| `feature/anin-export-filter` | Anin |
| `feature/irfan-logging` | Irfan |

---

## 📄 Lisensi

Project ini dibuat untuk keperluan Tugas Praktikum Pemrograman Berbasis Objek.

---
