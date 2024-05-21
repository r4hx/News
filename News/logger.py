import datetime
import logging
from os import makedirs
from pathlib import Path

import pytz

from News.settings import BASE_DIR, LOG_DIR, LOG_LEVEL, TIME_ZONE


def make_logger(name: str = "main") -> logging.Logger:
    """
    Создать логер
    """
    current_date = datetime.datetime.now(
        tz=pytz.timezone(TIME_ZONE),
    ).strftime("%Y/%m/%d")
    log_filename = f"{name}.log"
    log_directory_path = Path(BASE_DIR) / LOG_DIR / current_date
    log_path = Path(BASE_DIR) / LOG_DIR / current_date / log_filename
    if log_directory_path.exists() is False:
        makedirs(log_directory_path, exist_ok=True)
    logger = logging.getLogger(name=name)
    logger.setLevel(level=LOG_LEVEL)
    file_handler = logging.FileHandler(str(log_path), mode="a")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger
