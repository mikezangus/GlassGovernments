import os


def ensure_dir_exists(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def load_data_dir(project_dir: str):
    data_dir = os.path.join(project_dir, "data")
    ensure_dir_exists(data_dir)
    return data_dir


def load_data_cleaning_dir(project_dir: str):
    data_cleaning_dir = os.path.join(project_dir, "data_cleaning")
    ensure_dir_exists(data_cleaning_dir)
    return data_cleaning_dir


def load_data_collecting_dir(project_dir: str):
    data_collecting_dir = os.path.join(project_dir, "data_collecting")
    ensure_dir_exists(data_collecting_dir)
    return data_collecting_dir


def load_data_uploading_dir(project_dir: str):
    data_uploading_dir = os.path.join(project_dir, "data_uploading")
    ensure_dir_exists(data_uploading_dir)
    return data_uploading_dir


def load_us_states_dir(project_dir: str):
    us_states_dir = os.path.join(project_dir, "us_states")
    ensure_dir_exists(us_states_dir)
    return us_states_dir


def load_user_inputs_dir(project_dir: str):
    user_inputs_dir = os.path.join(project_dir, "user_inputs")
    ensure_dir_exists(user_inputs_dir)
    return user_inputs_dir


def load_downloads_container_dir(data_dir: str):
    downloads_container_dir = os.path.join(data_dir, "downloads_container")
    ensure_dir_exists(downloads_container_dir)
    return downloads_container_dir


def load_source_data_dir(data_dir: str):
    source_data_dir = os.path.join(data_dir, "source")
    ensure_dir_exists(source_data_dir)
    return source_data_dir


def load_raw_data_dir(data_dir: str):
    raw_data_dir = os.path.join(data_dir, "raw")
    ensure_dir_exists(raw_data_dir)
    return raw_data_dir


def load_cleaned_data_dir(data_dir: str):
    cleaned_data_dir = os.path.join(data_dir, "cleanx")
    ensure_dir_exists(cleaned_data_dir)
    return cleaned_data_dir