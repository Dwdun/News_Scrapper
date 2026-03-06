import logging
import logging.handlers
import os
import time
import functools


# Set up logging
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(nama: str) -> logging.Logger:
    logger = logging.getLogger(nama)
    logger.setLevel(logging.DEBUG)

    # memastikan tidak ada handler ganda
    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
            )
        log_file_path = os.path.join(LOG_DIR, "app.log")

        # RotatingFileHandler untuk mengelola ukuran file log
        file_handler = logging.handlers.RotatingFileHandler(
            log_file_path, maxBytes=5*1024*1024, backupCount=3
            )

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    return logger

# retry decorator untuk menangani kegagalan sementara
def retry(max_attempts=3, delay=2):
    def decorator(func):
        log = get_logger(func.__module__)
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    log.warning(f"Attempt {attempts} failed for {func.__name__}: {e}")
                    
                    if attempts < max_attempts:
                        time.sleep(delay)

                    else:
                        log.error(f"Function {func.__name__} failed after {max_attempts} attempts")
                        return None

        return wrapper
    return decorator

def handle_selenium_error(e: Exception, url: str = "") -> str:
    try:
        from selenium.common.exceptions import (
            NoSuchElementException,
            TimeoutException,
            WebDriverException
        )
    except ImportError: return f'Error: {e}'

    log = get_logger('error_handler')

    if isinstance(e, TimeoutException):
        msg = f"Timeout while accessing {url}: {e}"

    elif isinstance(e, NoSuchElementException):
        msg = f"Element not found while accessing {url}: {e}"

    elif isinstance(e, WebDriverException):
        msg = f"WebDriver error: {getattr(e, 'msg', str(e))}"

    else:
        msg = f"Error [{type(e).__name__}]: {e}"
    log.error(msg)
    return msg
    