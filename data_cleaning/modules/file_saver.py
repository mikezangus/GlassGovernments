import os
from directories import source_data_dir, cleaned_data_dir


def save_cleaned_file(year, state, district, file_name):
    
    source_file_path = os.path.join(source_data_dir, year, state, district, file_name)
    cleaned_file_dir = os.path.join(cleaned_data_dir, year, state, district)

    print(f"Starting to clean file: {file_name}")
    cleaned_file_name = file_name.replace("source", "cleanx")
    clean_file = process_raw_data(source_file_name = file_name, source_file_path = source_file_path)
    print(f"Finished cleaning file: {cleaned_file_name}")
    cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    os.makedirs(cleaned_file_dir, exist_ok = True)
    clean_file.to_csv(path_or_buf = cleaned_file_path, index = False)
    print(f"Saved cleaned file to: {cleaned_file_dir}\n")