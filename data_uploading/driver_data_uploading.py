import os
import sys

from modules.db_loader import load_db
from modules.data_type_converter import covert_data_types
from modules.cleaned_file_path_constructor import construct_cleaned_file_path
from modules.data_uploader import upload_data

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import user_inputs_dir, cleaned_data_dir
sys.path.append(user_inputs_dir)
from driver_user_inputs import main as get_user_inputs


def main():
    year, chamber, state, district, cleaned_file_name = get_user_inputs(data_source = "files", action = "upload")
    candidate_info = cleaned_file_name.split("_")
    _, _, _, last_name, first_name, _ = candidate_info
    db = load_db(project_dir = project_dir)
    cleaned_file_path = construct_cleaned_file_path(cleaned_data_dir = cleaned_data_dir, cleaned_file_name = cleaned_file_name, year = year, chamber = chamber, state = state, district = district)
    data = covert_data_types(cleaned_file_path = cleaned_file_path)
    upload_data(db = db, data = data, year = year, chamber = chamber, first_name = first_name, last_name = last_name)


if __name__ == "__main__":
    main()