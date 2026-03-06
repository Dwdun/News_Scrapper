import dateparser

def parse_date(date_str):
    """
    Fungsi untuk mengubah teks tanggal menjadi tipe objek date.
    """
    # Jika teks tanggal kosong atau tidak ada (None), kembalikan None
    if not date_str:
        return None
    
    try:
        # Parsing teks tanggal, bahasa Indonesia dan Inggris
        parsed_date = dateparser.parse(date_str, languages=["id", "en"])
    except Exception:
        # Menangkap error jika gagal
        return None
    
    # Format tanggal (YYYY-MM-DD)
    if parsed_date:
        return parsed_date.date()
    
    # Kembalikan None, jika gagal diparsing atau hasilnya None
    return None

def filter_by_date(articles, start_date, end_date):
    """
    Fungsi untuk menyaring daftar artikel berdasarkan rentang tanggal.
    """
    # Jika tanggal awal atau tanggal akhir kosong, kembalikan semua artikel
    if not start_date or not end_date:
        return articles
    
    # Ubah jika start_date atau end_date bertipe datetime menjadi date
    if hasattr(start_date, 'date'):
        start_date = start_date.date()
    if hasattr(end_date, 'date'):
        end_date = end_date.date()
    
    # List untuk menyimpan artikel yang sesuai
    filtered_articles = []
    
    # Cek tiap artikel di daftar
    for article in articles:
        # Ubah teks tanggal artikel menjadi tipe date
        article_date = parse_date(article.get('date', ''))
        
        # Jika hasil parse_date None, jangan dimasukkan ke hasil
        if article_date is None:
            continue
            
        # Hanya artikel dengan tanggal valid yang dibandingkan
        if start_date <= article_date <= end_date:
            # Masukkan artikel ke hasil
            filtered_articles.append(article)
            
    # Kembalikan daftar artikel yang sudah sesuai tanggal
    return filtered_articles
