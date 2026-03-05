import logging
import logging.handlers
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "Logs(irfan)")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("scraping_logger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

log_file_path = os.path.join(LOG_DIR, "scraper.log")

file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)