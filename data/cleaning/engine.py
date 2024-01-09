import os
import sys

from modules.column_arranger import arrange_columns
from modules.column_injector import inject_columns
from modules.column_renamer import rename_columns
from modules.file_loader import load_file
from modules.file_saver import save_file

cleaning_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(cleaning_dir)
sys.path.append(data_dir)
from data_directories import load_raw_files_dir, load_cleaned_files_dir


def clean_one_candidate(candidate: str, i: int, candidate_count: int):

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    input_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name, party = input_file_name.split("_")[3:6]

    subject = f"[{(i + 1):,}/{candidate_count:,}] {year} {state}-{district} {first_name} {last_name}"

    input_files_dir = load_raw_files_dir()
    data, raw_file_loaded = load_file(subject, year, chamber, state, input_file_name, input_files_dir, district)
    if not raw_file_loaded:
        return False
    elif data.empty:
        return False
    
    data = inject_columns(data, state, chamber, district, last_name, first_name, party)

    data = rename_columns(data)

    data = arrange_columns(data)

    output_files_dir = load_cleaned_files_dir()
    save_file(data, subject, year, chamber, state, input_file_name, output_files_dir, district)
    
    return True