import csv

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
