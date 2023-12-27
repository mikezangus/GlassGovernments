import logging
import os
import sys
from datetime import datetime
from .message_writer import write_success_message, write_failure_message


def create_log_file():
    action = "create log file"
    try:
        current_datetime = datetime.now()
        year = str(current_datetime.year)
        month = str(current_datetime.month)
        current_datetime_str = datetime.now().strftime("%Y_%m_%d_%H-%M-%S")
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        sys.path.append(parent_dir)
        log_dir = os.path.join(parent_dir, "logs", year, month)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        log_file_name = f"scraper_log_{current_datetime_str}.log"
        log_file_path = os.path.join(log_dir, log_file_name)
        logging.basicConfig(
            filename = log_file_path,
            level = logging.INFO,
            format = "%(asctime)s - %(levelname)s - %(message)s"
        )
        message = f"{write_success_message(action = action)} at {log_file_path}"
        print(message)
        return True
    except:
        message = write_failure_message(action = action)
        print(message)
        return False