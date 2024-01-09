import os


def construct_input_file_path(input_files_dir: str, input_file_name: str, year: str, chamber: str, state: str, district: str):
    if chamber.lower() == "house":
        input_file_path = os.path.join(input_files_dir, year, chamber, state, district, input_file_name)
    elif chamber.lower() == "senate":
        input_file_path = os.path.join(input_files_dir, year, chamber, state, input_file_name)
    return input_file_path