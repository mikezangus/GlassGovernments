import os
import sys

from modules.address_converter import convert_addresses_to_coordinates
from modules.column_arranger import arrange_columns
from modules.file_loader import load_file
from modules.file_saver import save_file

converting_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(converting_dir)
sys.path.append(data_dir)
from data_directories import load_cleaned_files_dir, load_converted_files_dir


def convert_one_candidate(candidate: str, i: int, candidate_count: int, purgatory_status: bool):

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    input_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name = input_file_name.split("_")[3:5]

    subject = f"[{(i + 1):,}/{candidate_count:,}] {year} {state}-{district} {first_name} {last_name}"

    input_files_dir = load_cleaned_files_dir()
    data, _ = load_file(subject, year, chamber, state, input_file_name, input_files_dir, district)

    data, purgatory_candidate = convert_addresses_to_coordinates(data, subject, candidate, purgatory_status)
    if purgatory_candidate:
        return False, purgatory_candidate
    
    data = arrange_columns(data)

    output_files_dir = load_converted_files_dir()
    save_file(data, subject, year, chamber, state, input_file_name, output_files_dir, district)
    
    return True, None