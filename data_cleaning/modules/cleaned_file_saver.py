import os


def save_cleaned_file(data, year: str, chamber: str, state: str, raw_file_name: str, cleaned_data_dir: str, district: str = None):
    cleaned_file_name = raw_file_name.replace("source", "cleanx")
    if district:
        cleaned_file_dir = os.path.join(cleaned_data_dir, year, chamber, state, district)
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    else:
        cleaned_file_dir = os.path.join(cleaned_data_dir, year, chamber, state)
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    cleaned_file = data
    cleaned_file.to_csv(cleaned_file_path, index = False)

