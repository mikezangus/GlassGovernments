import os


def construct_cleaned_file_path(cleaned_data_dir, cleaned_file_name, year, chamber, state, district):
    if chamber.lower() == "house":
        cleaned_file_path = os.path.join(cleaned_data_dir, year, chamber, state, district, cleaned_file_name)
    elif chamber.lower() == "senate":
        cleaned_file_path = os.path.join(cleaned_data_dir, year, chamber, state, cleaned_file_name)
    return cleaned_file_path