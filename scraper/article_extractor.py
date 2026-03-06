from selenium.webdriver.common.by import By


def extract_title(driver):
    """Ekstrak judul artikel dengan fallback selector."""
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
    """Ekstrak tanggal artikel dengan text selector dasar."""
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


def extract_content(driver):
    """Ekstrak konten artikel dari paragraf."""
    content_selectors = [
        'article p', '.detail__body-text p', '.read__content p',
        '.article-content p', '.post-content p', '.entry-content p',
        'main p',
    ]

    for sel in content_selectors:
        els = driver.find_elements(By.CSS_SELECTOR, sel)
        if els:
            paragraphs = [el.text.strip() for el in els if el.text.strip()]
            if paragraphs:
                return '\n'.join(paragraphs)

    return None
