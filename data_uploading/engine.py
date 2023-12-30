import os
import sys

from modules.db_loader import load_db
from modules.cleaned_file_path_constructor import construct_cleaned_file_path
from modules.data_type_converter import covert_data_types
from modules.data_uploader import upload_data

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import cleaned_data_dir


def upload_one_candidate(year: str, chamber: str, state: str, district: str, candidate: str):
    candidate_info = candidate.split("_")
    _, _, _, last_name, first_name, _, _ = candidate_info
    db = load_db(project_dir = project_dir)
    cleaned_file_path = construct_cleaned_file_path(cleaned_data_dir = cleaned_data_dir, cleaned_file_name = candidate, year = year, chamber = chamber[0], state = state[0], district = district[0])
    data = covert_data_types(cleaned_file_path = cleaned_file_path)
    upload_data(db = db, data = data, year = year, chamber = chamber, first_name = first_name, last_name = last_name)