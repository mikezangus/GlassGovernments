import os


data_dir = os.path.dirname(os.path.abspath(__file__))


def ensure_dir_exists(dir_path: str):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def load_user_inputs_dir():
    user_inputs_dir = os.path.join(data_dir, "user_inputs")
    ensure_dir_exists(user_inputs_dir)
    return user_inputs_dir


def load_collecting_dir():
    collecting_dir = os.path.join(data_dir, "collecting")
    ensure_dir_exists(collecting_dir)
    return collecting_dir


def load_cleaning_dir():
    cleaning_dir = os.path.join(data_dir, "cleaning")
    ensure_dir_exists(cleaning_dir)
    return cleaning_dir


def load_converting_dir():
    converting_dir = os.path.join(data_dir, "converting")
    ensure_dir_exists(converting_dir)
    return converting_dir


def load_purgatory_list_dir():
    purgatory_list_dir = os.path.join(data_dir, "converting", "purgatory_lists")
    ensure_dir_exists(purgatory_list_dir)
    return purgatory_list_dir


def load_data_uploading_dir():
    uploading_dir = os.path.join(data_dir, "uploading")
    ensure_dir_exists(uploading_dir)
    return uploading_dir


def load_downloads_container_dir():
    downloads_container_dir = os.path.join(data_dir, "data_files", "downloads_container")
    ensure_dir_exists(downloads_container_dir)
    return downloads_container_dir


def load_raw_files_dir():
    raw_data_dir = os.path.join(data_dir, "data_files", "raw")
    ensure_dir_exists(raw_data_dir)
    return raw_data_dir


def load_cleaned_files_dir():
    cleaned_data_dir = os.path.join(data_dir, "data_files", "cleaned")
    ensure_dir_exists(cleaned_data_dir)
    return cleaned_data_dir


def load_converted_files_dir():
    converted_data_dir = os.path.join(data_dir, "data_files", "converted") 
    ensure_dir_exists(converted_data_dir)
    return converted_data_dir