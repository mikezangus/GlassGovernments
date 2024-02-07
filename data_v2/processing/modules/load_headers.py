import os
import sys
from pathlib import Path

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_headers_dir


def load_headers(file_type: str) -> list:
    dir = get_headers_dir()
    path = os.path.join(dir, f"{file_type}_header_file.csv")
    with open(path, "r") as header_file:
        headers = header_file.readline().strip().split(",")
    return headers
