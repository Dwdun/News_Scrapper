import logging
import logging.handlers
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "Logs(irfan)")
os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("scraping_logger")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )

