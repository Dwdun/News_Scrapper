from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import os
import time


def setup_driver():
    import shutil
    
    options = Options()
    options.binary_location = '/usr/bin/brave-browser'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')

    browsers = [
        ('Google Chrome', ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable']),
        ('Brave', ['/usr/bin/brave-browser', '/usr/bin/brave-browser-stable']),
        ('Chromium', ['/usr/bin/chromium', '/usr/bin/chromium-browser']),
        ('Edge', ['/usr/bin/microsoft-edge', '/usr/bin/microsoft-edge-stable']),
    ]

    detected = None
    for name, paths in browsers:
        for path in paths:
            if shutil.which(path) or os.path.isfile(path):
                detected = (name, path)
                break
        if detected:
            break

    if detected:
        print(f"Browser terdeteksi: {detected[0]} ({detected[1]})")
        options.binary_location = detected[1]
    else:
        print("Tidak ada browser khusus terdeteksi, menggunakan default ChromeDriver.")

    driver = webdriver.Chrome(options=options)
    return driver


if __name__ == '__main__':
    driver = setup_driver()
    print("Browser berhasil dijalankan!")
    driver.quit()
