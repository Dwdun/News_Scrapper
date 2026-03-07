import json
import os
import sys
from datetime import datetime, timedelta
from dateutil import parser as dateparser


def load_articles(filepath="data.json"):
    """Load artikel dari file JSON."""
    if not os.path.exists(filepath):
        print(f"File {filepath} tidak ditemukan.")
        return []

    with open(filepath, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("File JSON tidak valid.")
            return []

    return data.get("list", [])


def parse_date(date_str):
    """Parse string tanggal ke datetime object. Return None jika gagal."""
    if not date_str:
        return None
    try:
        return dateparser.parse(date_str, ignoretz=True)
    except (ValueError, TypeError):
        pass

    # Fallback: format Indonesia seperti "21 Juni 2024 | 12.00 WIB"
    try:
        bulan_id = {
            'januari': 'January', 'februari': 'February', 'maret': 'March',
            'april': 'April', 'mei': 'May', 'juni': 'June',
            'juli': 'July', 'agustus': 'August', 'september': 'September',
            'oktober': 'October', 'november': 'November', 'desember': 'December'
        }
        cleaned = date_str.split('|')[0].strip()
        cleaned = cleaned.replace(' WIB', '').replace(' WITA', '').replace(' WIT', '')
        for id_name, en_name in bulan_id.items():
            cleaned = cleaned.replace(id_name.capitalize(), en_name)
            cleaned = cleaned.replace(id_name, en_name)
        return dateparser.parse(cleaned, ignoretz=True)
    except (ValueError, TypeError):
        return None



def search_by_date(articles, target_date):
    """Cari artikel berdasarkan tanggal tertentu (YYYY-MM-DD)."""
    hasil = []
    for article in articles:
        dt = parse_date(article.get("date"))
        if dt and dt.date() == target_date.date():
            hasil.append(article)
    return hasil


def search_by_range(articles, start_date, end_date):
    """Cari artikel berdasarkan range tanggal (inklusif)."""
    hasil = []
    for article in articles:
        dt = parse_date(article.get("date"))
        if dt and start_date.date() <= dt.date() <= end_date.date():
            hasil.append(article)
    return hasil


def display_results(articles):
    """Tampilkan hasil pencarian."""
    if not articles:
        print("\n  Tidak ada artikel ditemukan.\n")
        return

    # Urutkan berdasarkan tanggal (terbaru dulu)
    articles.sort(key=lambda a: parse_date(a.get("date")) or datetime.min, reverse=True)

    print(f"\n{'='*60}")
    print(f"  Ditemukan {len(articles)} artikel")
    print(f"{'='*60}\n")

    for i, article in enumerate(articles, 1):
        title = article.get("title", "Tanpa judul")
        date = article.get("date", "-")
        url = article.get("url", "-")
        authors = ", ".join(article.get("authors", [])) or "-"
        content = article.get("content", "")

        preview = ""
        if content:
            preview = content[:120].replace("\n", " ")
            if len(content) > 120:
                preview += "..."

        print(f"  {i}. {title}")
        print(f"{date}")
        print(f"{authors}")
        if preview:
            print(f"{preview}")
        print(f"{url}")
        print()


def parse_input_date(text):
    """Parse input tanggal dari user. Mendukung YYYY-MM-DD dan shortcut."""
    text = text.strip().lower()

    today = datetime.now()

    # Shortcut
    if text == "hari ini" or text == "today":
        return today
    elif text == "kemarin" or text == "yesterday":
        return today - timedelta(days=1)
    elif text.startswith("minggu ini") or text == "this week":
        return None

    try:
        return dateparser.parse(text, ignoretz=True)
    except (ValueError, TypeError):
        return None


def main():
    """Menu utama pencarian artikel."""
    articles = load_articles()
    if not articles:
        print("Tidak ada data artikel.")
        return

    print(f"\nPencarian Artikel ({len(articles)} artikel tersimpan)")
    print(f"{'='*50}")
    print("  Pilihan pencarian:")
    print("  1. Cari berdasarkan tanggal tertentu")
    print("  2. Cari berdasarkan range tanggal")
    print("  3. Tampilkan semua artikel minggu ini")
    print("  4. Tampilkan semua artikel hari ini")
    print("  0. Keluar")
    print(f"{'='*50}")

    pilihan = input("\nPilih [0-4]: ").strip()

    today = datetime.now()

    if pilihan == "1":
        print("\n  Format: YYYY-MM-DD (contoh: 2026-03-05)")
        print("  Shortcut: 'hari ini', 'kemarin'")
        inp = input("  Tanggal: ").strip()

        target = parse_input_date(inp)
        if not target:
            print("  Format tanggal tidak valid.")
            return

        print(f"\n  Mencari artikel tanggal {target.strftime('%Y-%m-%d')}...")
        hasil = search_by_date(articles, target)
        display_results(hasil)

    elif pilihan == "2":
        print("\n  Format: YYYY-MM-DD (contoh: 2026-03-01)")
        inp_start = input("  Dari tanggal : ").strip()
        inp_end = input("  Sampai tanggal: ").strip()

        start = parse_input_date(inp_start)
        end = parse_input_date(inp_end)

        if not start or not end:
            print("  Format tanggal tidak valid.")
            return

        if start > end:
            start, end = end, start

        print(f"\n  Mencari artikel {start.strftime('%Y-%m-%d')} s/d {end.strftime('%Y-%m-%d')}...")
        hasil = search_by_range(articles, start, end)
        display_results(hasil)

    elif pilihan == "3":
        start_of_week = today - timedelta(days=today.weekday())
        print(f"\n  Artikel minggu ini ({start_of_week.strftime('%Y-%m-%d')} s/d {today.strftime('%Y-%m-%d')})...")
        hasil = search_by_range(articles, start_of_week, today)
        display_results(hasil)

    elif pilihan == "4":
        print(f"\n  Artikel hari ini ({today.strftime('%Y-%m-%d')})...")
        hasil = search_by_date(articles, today)
        display_results(hasil)

    elif pilihan == "0":
        print("Keluar.")
        return

    else:
        print("Pilihan tidak valid.")


if __name__ == '__main__':
    main()
