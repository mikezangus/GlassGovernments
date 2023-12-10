import logging
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from project_utilities import downloads_container_dir, raw_data_dir


def prepare_download_path():
    try:
        if not os.path.exists(downloads_container_dir):
            os.makedirs(downloads_container_dir)
        for file_name in os.listdir(downloads_container_dir):
            file_path = os.path.join(downloads_container_dir, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)
        return True
    except Exception as e:
        print(f"Error preparing download path. Exception: {e}")
        return False


def save_downloaded_file(year, state, district, last_name, first_name, party):
    if not os.listdir(downloads_container_dir):
        print(f"No file found in {downloads_container_dir}")
        logging.info(f"Download failed for candidate: {first_name} {last_name} ({party}), {state}-{str(district).zfill(2)}")
        return False
    for downloaded_file_name in os.listdir(downloads_container_dir):
        downloaded_file_path = os.path.join(downloads_container_dir, downloaded_file_name)
        if os.path.isfile(downloaded_file_path):
            destination_dir = os.path.join(raw_data_dir, year, state, district)
            os.makedirs(destination_dir, exist_ok = True)
            formatted_file_name = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_raw.csv"
            destination_file_path = os.path.join(destination_dir, formatted_file_name)
            os.rename(downloaded_file_path, destination_file_path)
            print(f"File created at {destination_file_path}")
            return True