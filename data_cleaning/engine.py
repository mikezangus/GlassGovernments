import os
import sys

from modules.address_converter import convert_addresses_to_coordinates
from modules.cleaned_file_saver import save_cleaned_file
from modules.column_arranger import arrange_columns
from modules.column_injector import inject_columns
from modules.column_renamer import rename_columns
from modules.raw_file_loader import load_raw_file

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import load_data_dir, load_raw_data_dir, load_cleaned_data_dir



def clean_one_candidate(candidate: str, i: int, candidate_count: int, purgatory: bool):

    data_dir = load_data_dir(project_dir)
    raw_data_dir = load_raw_data_dir(data_dir)
    cleaned_data_dir = load_cleaned_data_dir(data_dir)

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    raw_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name, party = raw_file_name.split("_")[3:6]

    subject = f"[{(i + 1):,}/{candidate_count:,}] {year} {state}-{district} {first_name} {last_name}"

    data, raw_file_loaded = load_raw_file(subject, year, chamber, state, raw_file_name, raw_data_dir, district)
    if not raw_file_loaded:
        return False, None
    elif data.empty:
        return False, None
    data = inject_columns(data, state, chamber, district, last_name, first_name, party)
    data = rename_columns(data)
    data, purgatory_candidate = convert_addresses_to_coordinates(data, subject, candidate, purgatory)
    if purgatory_candidate:
        return False, purgatory_candidate
    elif data.empty:
        return False, None
    data = arrange_columns(data)
    save_cleaned_file(data, subject, year, chamber, state, raw_file_name, cleaned_data_dir, district)
    return True, None
