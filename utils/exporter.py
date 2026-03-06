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
            
        # Menulis setiap artikel ke baris berikutnya di Excel
        for i, row in enumerate(data, 1):
            # i = nomor urut mulai dari 1
            # row.get(k, "") mengambil nilai dari field k, jika kosong maka ""
            ws.append([i] + [row.get(k, "") for k in FIELDS])
            
        # Mengatur lebar kolom otomatis agar teks tidak terpotong
        for col in ws.columns:
            max_length = int(0)
            # Mengambil huruf kolom (A, B, C, dst.)
            column_letter = col[0].column_letter
            
            # Mencari teks paling panjang di dalam satu baris kolom
            for cell in col:
                try:
                    if str(cell.value):
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                except:
                    pass
            
            # Menetapkan lebar kolom ditambah sedikit ruang ekstra (contoh: +2)
            ws.column_dimensions[column_letter].width = int(max_length + 2)

        # Menyimpan file Excel ke lokasi yang ditentukan
        wb.save(filepath)
        
        # File Excel berhasil diekspor
        return True
            
    except Exception:
        return False
