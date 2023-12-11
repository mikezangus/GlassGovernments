import logging
import os
import sys
from message_writer import write_failure_message

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from directories import downloads_container_dir, raw_data_dir


def prepare_download_path(state, district, first_name, last_name):
    action = "prepare download path"
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    try:
        if not os.path.exists(downloads_container_dir):
            os.makedirs(downloads_container_dir)
        for file_name in os.listdir(downloads_container_dir):
            file_path = os.path.join(downloads_container_dir, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        return True
    except Exception as e:
        message = write_failure_message(action = action, subject = subject, exception = e)
        print(message)
        logging.info(msg = message)
        return False


def save_downloaded_file(year, state, district, last_name, first_name, party):
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    action = f"find file in {downloads_container_dir}"
    if not os.listdir(downloads_container_dir):
        print(f"No file found in {downloads_container_dir}")
        logging.info(f"Download failed for candidate: {first_name} {last_name} ({party}), {state}-{district}")
        return False
    action = f"save file to {raw_data_dir}"
    for downloaded_file_name in os.listdir(downloads_container_dir):
        downloaded_file_path = os.path.join(downloads_container_dir, downloaded_file_name)
        if os.path.isfile(downloaded_file_path):
            destination_dir = os.path.join(raw_data_dir, year, state, district)
            os.makedirs(destination_dir, exist_ok = True)
            formatted_file_name = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_raw.csv"
            destination_file_path = os.path.join(destination_dir, formatted_file_name)
            os.rename(downloaded_file_path, destination_file_path)
            print(f"File saved to {destination_file_path}")
            return True
    else:
        message = write_failure_message(action = action, subject = subject)
        print(message)
        logging.info(msg = message)
        return False