import logging
import os
import sys
from .message_writer import write_failure_message, write_success_message

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(parent_dir)
sys.path.append(project_dir)
from project_directories import downloads_container_dir, raw_data_dir


def clear_downloads_container():
    if not os.path.exists(downloads_container_dir):
        os.makedirs(downloads_container_dir)
        print(f"Downloads container crated at {downloads_container_dir}")
    for file_name in os.listdir(downloads_container_dir):
        file_path = os.path.join(downloads_container_dir, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print("Cleared downloads container")


def find_downloaded_file():
    action = f"find file in {downloads_container_dir}"
    if os.listdir(downloads_container_dir):
        message = write_success_message(action = action)
        print(message)
        return True
    return False


def save_downloaded_file(year: str, chamber: str, state: str, district: str, last_name: str, first_name: str, party: str):
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    action = f"save file to {raw_data_dir}"
    for downloaded_file_name in os.listdir(downloads_container_dir):
        downloaded_file_path = os.path.join(downloads_container_dir, downloaded_file_name)
        if os.path.isfile(downloaded_file_path):
            destination_dir = os.path.join(raw_data_dir, year, chamber, state, district)
            os.makedirs(destination_dir, exist_ok = True)
            formatted_file_name = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_raw.csv"
            destination_file_path = os.path.join(destination_dir, formatted_file_name)
            os.rename(downloaded_file_path, destination_file_path)
            print(f"File saved to {destination_file_path}")
            return True
    message = write_failure_message(action = action, subject = subject)
    print(message)
    logging.info(message)
    return False