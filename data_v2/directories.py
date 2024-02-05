import os
from pathlib import Path


def verify_dir_exists(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok = True)


def get_project_dir() -> str:
    directories_dir = Path(__file__).resolve().parent
    project_dir = directories_dir.parent
    return project_dir


def get_data_files_dir():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dir = os.path.join(current_dir, "data_files")
    verify_dir_exists(dir)
    return dir


def get_raw_dir():
    dir = os.path.join(get_data_files_dir(), "raw")
    verify_dir_exists(dir)
    return dir


def get_cleaned_dir():
    dir = os.path.join(get_data_files_dir(), "cleaned")
    verify_dir_exists(dir)
    return dir


def get_headers_dir():
    dir = os.path.join(get_data_files_dir(), "headers")
    verify_dir_exists(dir)
    return dir


def get_src_file_dir(year: str, file_type: str):
    dir = os.path.join(get_raw_dir(), year, file_type)
    verify_dir_exists(dir)
    return dir


def get_config_file_path() -> str:
    dir = get_project_dir()
    path = os.path.join(dir, "config.json")
    return path