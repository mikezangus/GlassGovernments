import logging
import os
from datetime import datetime
from .message_writer import write_success_message, write_failure_message


current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.dirname(current_dir)
data_collecting_dir = os.path.dirname(modules_dir)


def create_log_file():
    action = "create log file"
    try:
        current_datetime = datetime.now()
        year = str(current_datetime.year)
        month = str(current_datetime.month).zfill(2)
        day = str(current_datetime.day).zfill(2)
        current_datetime_str = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
        log_dir = os.path.join(data_collecting_dir, "logs", year, month, day)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_name = f"scraper_log_{current_datetime_str}.log"
        log_file_path = os.path.join(log_dir, log_file_name)
        logging.basicConfig(
            filename = log_file_path,
            level = logging.INFO,
            format = "%(asctime)s - %(levelname)s - %(message)s"
        )
        message = f"{write_success_message(action)} at:\n{log_file_path}"
        print(message)
        return True
    except Exception as e:
        message = write_failure_message(action, exception = e)
        print(message)
        return False