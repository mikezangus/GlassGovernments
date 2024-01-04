import os
import sys

from modules.db_loader import load_db
from modules.cleaned_file_path_constructor import construct_cleaned_file_path
from modules.data_type_converter import covert_data_types
from modules.data_uploader import upload_data


def upload_one_candidate(candidate: str, cleaned_data_dir: str):

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    cleaned_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name, party = cleaned_file_name.split("_")[3:6]

    subject = f"{state}-{district} candidate {first_name} {last_name}"

    db = load_db()
    cleaned_file_path = construct_cleaned_file_path(cleaned_data_dir, cleaned_file_name, year, chamber, state, district)
    data = covert_data_types(cleaned_file_path)
    upload_data(db, data, subject, year, chamber)