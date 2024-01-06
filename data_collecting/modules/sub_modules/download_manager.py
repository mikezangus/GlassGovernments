import logging
import os
import sys
from .message_writer import write_success_message, write_failure_message

current_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.dirname(current_dir)
data_collecting_dir = os.path.dirname(modules_dir)
project_dir = os.path.dirname(data_collecting_dir)
sys.path.append(project_dir)
from project_directories import load_data_dir, load_downloads_container_dir, load_raw_data_dir


data_dir = load_data_dir(project_dir)
downloads_container_dir = load_downloads_container_dir(data_dir)
raw_data_dir = load_raw_data_dir(data_dir)


def clear_downloads_container():
    try:
        for file_name in os.listdir(downloads_container_dir):
            file_path = os.path.join(downloads_container_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return True
    except:
        message = write_failure_message("clear downloads container")
        print(message)
        return False


def find_downloaded_file(subject):
    if os.listdir(downloads_container_dir):
        message = write_success_message("find downloaded file", subject)
        print(message)
        return True
    message = write_failure_message("find downloaded file", subject)
    print(message)
    return False


def save_downloaded_file(subject, year: str, chamber: str, state: str, last_name: str, first_name: str, party: str, district: str = None):
    action = f"save file to {raw_data_dir}"
    for downloaded_file_name in os.listdir(downloads_container_dir):
        downloaded_file_path = os.path.join(downloads_container_dir, downloaded_file_name)
        if os.path.isfile(downloaded_file_path):
            if chamber.lower() == "house":
                destination_dir = os.path.join(raw_data_dir, year, chamber.lower(), state, district)
            elif chamber.lower() == "senate":
                destination_dir = os.path.join(raw_data_dir, year, chamber.lower(), state)
            os.makedirs(destination_dir, exist_ok = True)
            formatted_file_name = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_raw.csv"
            destination_file_path = os.path.join(destination_dir, formatted_file_name)
            os.rename(downloaded_file_path, destination_file_path)
            print(f"{subject} | Raw file saved to:\n{destination_file_path}")
            return True
    message = write_failure_message(action, subject)
    print(message)
    logging.info(message)
    return False