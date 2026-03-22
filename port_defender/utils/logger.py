# utils/logger.py

import logging
import os
from utils.config import LOG_FILE, LOG_LEVEL

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR
}

logging.basicConfig(
    filename=LOG_FILE,
    level=LEVEL_MAP.get(LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("PortDefender")

def log_info(msg):
    logger.info(msg)
    print(f"[INFO] {msg}")

def log_warning(msg):
    logger.warning(msg)
    print(f"[WARNING] {msg}")

def log_error(msg):
    logger.error(msg)
    print(f"[ERROR] {msg}")

def log_debug(msg):
    logger.debug(msg)
    print(f"[DEBUG] {msg}")