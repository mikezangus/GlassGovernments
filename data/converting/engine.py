import os
import sys

from modules.address_converter import convert_addresses_to_coordinates
from modules.address_counter import count_addresses
from modules.column_arranger import arrange_columns
from modules.file_loader import load_file
from modules.file_saver import save_file
from modules.purgatory_list_populator import populate_purgatory_file

converting_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(converting_dir)
sys.path.append(data_dir)
from data_directories import load_cleaned_files_dir, load_converted_files_dir


def convert_one_candidate(candidate: str, i: int, candidate_count: int, purgatory_status: bool):
        
    try:

        split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
        constituency = candidate[:split_index]
        input_file_name = candidate[split_index + 1:]
        year, chamber, state, district = constituency.split("_")
        last_name, first_name = input_file_name.split("_")[3:5]

        subject = f"[{(i + 1):,}/{candidate_count:,}] {year} {state}-{district} {first_name} {last_name}"

        input_files_dir = load_cleaned_files_dir()
        data, _ = load_file(subject, year, chamber, state, input_file_name, input_files_dir, district)

        data_length = count_addresses(data)

        if data_length >= 1000 and not purgatory_status:
            print("populating purgatory file")
            populate_purgatory_file(candidate)
            return True
        else:
            print("not populating purgatory file")

        data = convert_addresses_to_coordinates(data, subject)
        
        data = arrange_columns(data)

        output_files_dir = load_converted_files_dir()
        save_file(data, subject, year, chamber, state, input_file_name, output_files_dir, district)
        
        return True
    
    except:

        return False