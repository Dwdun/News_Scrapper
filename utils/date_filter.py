import dateparser

def parse_date(date_str):
    """
    Fungsi untuk mengubah teks tanggal menjadi tipe objek date.
    """
    # Jika teks tanggal kosong atau tidak ada (None), kembalikan None
    if not date_str:
        return None
    
    # Parsing teks tanggal, bahasa Indonesia dan Inggris
    parsed_date = dateparser.parse(date_str, languages=["id", "en"])
    
    # Format tanggal (YYYY-MM-DD)
    if parsed_date:
        return parsed_date.date()
    
    # Kembalikan None, jika gagal diparsing atau hasilnya None
    return None
