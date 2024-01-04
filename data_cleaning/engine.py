import os
import sys
from modules.raw_file_loader import load_raw_file
from modules.candidate_info_injector import inject_candidate_info
from modules.address_converter import convert_addresses_to_coordinates
from modules.column_arranger import arrange_columns
from modules.cleaned_file_saver import save_cleaned_file

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import load_data_dir, load_raw_data_dir, load_cleaned_data_dir
data_dir = load_data_dir(project_dir)
raw_data_dir = load_raw_data_dir(data_dir)
cleaned_data_dir = load_cleaned_data_dir(data_dir)


def clean_one_candidate(candidate: str):

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    raw_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name, party = raw_file_name.split("_")[3:6]

    subject = f"{state}-{district} candidate {first_name} {last_name}"

    data = load_raw_file(year, chamber, state, raw_file_name, raw_data_dir, district)
    data = inject_candidate_info(data, state, district, last_name, first_name, party)
    data = convert_addresses_to_coordinates(data, subject)
    data = arrange_columns(data)
    save_cleaned_file(data, year, chamber, state, raw_file_name, cleaned_data_dir, district)