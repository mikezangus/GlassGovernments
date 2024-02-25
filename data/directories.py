import os


current_dir = os.path.dirname(os.path.abspath(__file__))


def verify_dir_exists(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok = True)
    return


def get_project_dir() -> str:
    directories_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(directories_dir)
    return project_dir


def get_data_files_dir() -> str:
    dir = os.path.join(current_dir, "data_files")
    verify_dir_exists(dir)
    return dir


def get_raw_dir() -> str:
    dir = os.path.join(get_data_files_dir(), "raw")
    verify_dir_exists(dir)
    return dir


def get_raw_year_dir(year: str) -> str:
    dir = os.path.join(get_raw_dir(), year)
    verify_dir_exists(dir)
    return dir


def get_download_dir(year: str) -> str:
    dir = os.path.join(get_data_files_dir(), "downloads_containers", year)
    verify_dir_exists(dir)
    return dir


def get_headers_dir() -> str:
    dir = os.path.join(get_data_files_dir(), "headers")
    verify_dir_exists(dir)
    return dir


def get_src_file_dir(year: str, file_type: str) -> str:
    dir = os.path.join(get_raw_dir(), year, file_type)
    verify_dir_exists(dir)
    return dir


def get_config_file_path() -> str:
    path = os.path.join(current_dir, "config.json")
    return path


def get_states_all_file_path() -> str:
    path = os.path.join(current_dir, "geography", "usa", "states", "usa_states_all.json")
    return path