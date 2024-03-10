import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.directories import get_headers_dir


def load_headers(file_type: str) -> list:
    path = os.path.join(
        get_headers_dir(),
        f"{file_type}_header_file.csv"
    )
    with open(path, "r") as header_file:
        headers = header_file \
            .readline() \
            .strip()\
            .split(",")
    return headers
