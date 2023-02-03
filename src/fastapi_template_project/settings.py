"""
Settings
"""

import os

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
DATA_UPLOAD_DIR = os.path.join(DATA_DIR, "upload")
LOG_DIR = os.path.join(DATA_DIR, "logs")
LOG_SYSTEM = os.path.join(LOG_DIR, "system.log")
LOG_SIZE = 512 * 1024
LOG_HISTORY = 20
LOGGING_FMT = (
    "%(levelname)s %(asctime)s %(filename)s:%(lineno)s (%(funcName)s) - %(message)s"
)
LOGGING_USE_GZIP = True
UPLOAD_CHUNK_SIZE = 1024 * 64
IS_TEST = os.getenv("IS_TEST", "0") == "1"
API_KEY = os.getenv("API_KEY", "test")

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(DATA_UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)
