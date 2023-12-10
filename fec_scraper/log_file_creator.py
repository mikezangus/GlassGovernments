import logging
import os
from datetime import datetime


def create_log_file():
    current_datetime = datetime.now()
    year = str(current_datetime.year)
    month = str(current_datetime.month)
    current_datetime_str = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    log_dir = os.path.join(current_dir, "logs", year, month)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file_name = f"failed_downloads_{current_datetime_str}.log"
    log_file_path = os.path.join(log_dir, log_file_name)
    logging.basicConfig(
        filename = log_file_path,
        level = logging.INFO,
        format = "%(asctime)s - %(levelname)s - %(message)s"
    )