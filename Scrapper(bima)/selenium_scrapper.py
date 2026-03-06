from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json
import os
import time
def setup_driver():
    options = Options()
    options.binary_location = '/usr/bin/brave-browser'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    return driver
if __name__ == '__main__':
    driver = setup_driver()
    print("Browser berhasil dijalankan!")
    driver.quit()