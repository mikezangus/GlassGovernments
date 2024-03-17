import os


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.dirname(CURRENT_DIR)


def verify_dir_exists(dir: str) -> None:
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok = True)
    return


def get_data_files_dir() -> str:
    dir = os.path.join(
        DATA_DIR,
        "data_files"
    )
    verify_dir_exists(dir)
    return dir


def get_raw_dir() -> str:
    dir = os.path.join(
        get_data_files_dir(),
        "raw"
    )
    verify_dir_exists(dir)
    return dir


def get_headers_dir() -> str:
    dir = os.path.join(
        get_data_files_dir(),
        "headers"
    )
    verify_dir_exists(dir)
    return dir


def get_download_dir(year: str) -> str:
    dir = os.path.join(
        get_data_files_dir(),
        "downloads_containers",
        year
    )
    verify_dir_exists(dir)
    return dir


def get_raw_year_dir(year: str) -> str:
    dir = os.path.join(
        get_raw_dir(),
        year
    )
    verify_dir_exists(dir)
    return dir


def get_raw_file_dir(year: str, file_type: str) -> str:
    dir = os.path.join(
        get_raw_year_dir(year),
        file_type
    )
    verify_dir_exists(dir)
    return dir


def get_load_states_dir() -> str:
    return os.path.join(
        DATA_DIR,
        "geography",
        "usa",
        "states"
    )


def get_config_file_path() -> str:
    return os.path.join(DATA_DIR, "config.json")
