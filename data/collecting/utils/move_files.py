import os
import shutil
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COLLECTING_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.dirname(COLLECTING_DIR)
sys.path.append(DATA_DIR)
from utils.directories import get_headers_dir, get_raw_year_dir


def move_files(download_dir: str, election_year: str) -> bool:
    try:
        print("\nStarted moving all files")
        for file_name in os.listdir(download_dir):
            if "header" in file_name.lower():
                header_src_path = os.path.join(download_dir, file_name)
                header_dst_path = os.path.join(get_headers_dir(), file_name)
                shutil.move(header_src_path, header_dst_path)
                print(f"Finished moving {file_name} to\n{header_dst_path}")
            elif file_name.endswith(".zip"):
                year_src_path = os.path.join(download_dir, file_name)
                year_dst_path = os.path.join(get_raw_year_dir(election_year), file_name)
                shutil.move(year_src_path, year_dst_path)
                print(f"Finished moving {file_name} to\n{year_dst_path}")
        shutil.rmtree(download_dir)
        print("Finished moving all files")
        return True
    except Exception as e:
        print("Move Files | Error:", e)
        return False
