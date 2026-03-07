from selenium.webdriver.common.by import By
from newspaper import Article


def extract_article(html, url):
    result = {
        'title': None,
        'date': None,
        'content': None,
        'image': None,
        'authors': [],
        'url': url
    }

    try:
        article = Article(url)
        article.download(input_html=html)
        article.parse()

        result['title'] = article.title or None
        result['date'] = str(article.publish_date) if article.publish_date else None
        result['content'] = article.text[:600] + '...' if len(article.text) > 600 else article.text if article.text else None
        result['image'] = article.top_image or None
        result['authors'] = article.authors if article.authors else []

    except Exception as e:
        print(f"  newspaper4k gagal: {e}")

    return result


def extract_article_with_fallback(driver, url):
    html = driver.page_source
    result = extract_article(html, url)

    # Fallback ke CSS selector jika newspaper4k gagal ambil field tertentu
    if not result['title']:
        result['title'] = extract_title(driver)

    if not result['date']:
        result['date'] = extract_date(driver)

    if not result['content']:
        result['content'] = extract_content(driver)

    return result


# === Fallback Functions (CSS Selector) ===

def extract_title(driver):
    title_selectors = [
        'h1', 'h1.title', 'h1.detail__title', 'h1.read__title',
        'h1[itemprop="headline"]', '.article-title'
    ]

    for sel in title_selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            return els[0].text.strip()

    return None


def extract_date(driver):
    """Ekstrak tanggal artikel, prioritaskan elemen dengan attribute datetime."""

    # Fase 1: Elemen dengan attribute datetime (format ISO lebih konsisten)
    datetime_selectors = [
        'time[datetime]',
        '[itemprop="datePublished"][datetime]',
        'meta[property="article:published_time"]',
        '[data-datetime]',
    ]

    for sel in datetime_selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            value = (
                els[0].get_attribute('datetime')
                or els[0].get_attribute('content')
                or els[0].get_attribute('data-datetime')
            )
            if value and value.strip():
                return value.strip()

    # Fase 2: Fallback ke text content dari elemen tanggal umum
    text_selectors = [
        'time',
        '.date', '.publish-date', '.detail__date',
        '[class*="date"]',
        '[itemprop="datePublished"]',
        '.article__date', '.post-date', '.entry-date',
    ]

    for sel in text_selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            value = els[0].get_attribute('datetime') or els[0].text.strip()
            if value and value.strip():
                return value.strip()

    return None


def extract_content(driver, min_length=30, max_chars=600):
    """Ekstrak konten artikel, filter paragraf pendek, batasi hasil maksimal."""

    content_selectors = [
        'article p',
        '[itemprop="articleBody"] p',
        '.detail__body-text p',
        '.read__content p',
        '.article-content p',
        '.post-content p',
        '.entry-content p',
        '.content-detail p',
        'main p',
    ]

    for sel in content_selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            paragraphs = [
                el.text.strip() for el in els
                if el.text.strip() and len(el.text.strip()) > min_length
            ]

            if paragraphs:
                gabungan = '\n'.join(paragraphs)
                if len(gabungan) > max_chars:
                    gabungan = gabungan[:max_chars].rsplit(' ', 1)[0] + '...'
                return gabungan

    return None
