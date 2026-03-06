import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

# FIELDS: bagian data artikel yang mau dimasukkan ke file
FIELDS = ["title", "date", "content", "url"]

# HEADERS: judul kolom yang akan tampil di bagian atas file export
HEADERS = ["Judul", "Tanggal", "Isi", "URL"]

def export_to_csv(data, filepath):
    """
    Mengekspor daftar artikel ke dalam file format CSV.
    """
    try:
        # Membuka file CSV untuk ditulis
        with open(filepath, "w", newline="", encoding="utf-8-sig") as file:
            # Alat untuk menulis data artikel ke CSV sesuai kolom di FIELDS
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            
            # Menulis baris pertama CSV yang berisi nama kolom
            writer.writeheader()
            
            # Menambahkan setiap artikel ke dalam file CSV
            for row in data:
                # Mengambil data artikel sesuai field yang dibutuhkan, jika tidak ada biarkan kosong ""
                writer.writerow({k: row.get(k, "") for k in FIELDS})
                
        # File berhasil diexport
        return True
    
    except Exception:
        # Jika ada file yang gagal diekspor (error)
        return False

def export_to_excel(data, filepath):
    """
    Mengekspor daftar artikel ke dalam file format Excel
    """
    try:
        # Membuat file Excel baru
        wb = openpyxl.Workbook()
        
        # Mengambil sheet Excel yang akan kita isi data
        ws = wb.active
        
        # Mengganti nama sheet
        ws.title = "Hasil Scraping"
        
        # Menulis baris pertama sebagai header, tambahkan awalan kolom "No"
        ws.append(["No"] + HEADERS)
        
        # Mengatur tampilan header
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="0070C0", end_color="0070C0", fill_type="solid")
        header_alignment = Alignment(horizontal="center", vertical="center")
        
        # Menerapkan tampilan tersebut ke semua cell di baris pertama
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
        
    except Exception:
        return False
