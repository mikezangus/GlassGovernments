import logging
import os
from datetime import datetime


def create_log() -> None:
    now = datetime.now()
    year = str(now.year)
    month = str(now.month).zfill(2)
    day = str(now.day).zfill(2)
    now_text = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    coords_dir = os.path.dirname(__file__)
    log_dir = os.path.join(coords_dir, "logs", year, month, day)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_name = f"{now_text}.log"
    file_path = os.path.join(log_dir, file_name)
    logging.basicConfig(
        filename = file_path,
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )
    return
