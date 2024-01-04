import os


def construct_cleaned_file_path(cleaned_data_dir: str, cleaned_file_name: str, year: str, chamber: str, state: str, district: str):
    if chamber.lower() == "house":
        cleaned_file_path = os.path.join(cleaned_data_dir, year, chamber, state, district, cleaned_file_name)
    elif chamber.lower() == "senate":
        cleaned_file_path = os.path.join(cleaned_data_dir, year, chamber, state, cleaned_file_name)
    return cleaned_file_path