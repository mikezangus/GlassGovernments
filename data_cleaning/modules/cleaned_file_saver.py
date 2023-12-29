import os


def save_cleaned_file(data, raw_file_name, cleaned_data_dir, year, chamber, state, district = None):
    cleaned_file_name = raw_file_name.replace("source", "cleanx")
    if chamber.lower() == "house" and district:
        cleaned_file_dir = os.path.join(cleaned_data_dir, year, chamber, state, district)
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    elif chamber.lower() == "senate":
        cleaned_file_dir = os.path.join(cleaned_data_dir, year, chamber, state)
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    cleaned_file = data
    cleaned_file.to_csv(path_or_buf = cleaned_file_path, index = False)