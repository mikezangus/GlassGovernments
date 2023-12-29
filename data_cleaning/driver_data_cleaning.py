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
from project_directories import user_inputs_dir, raw_data_dir, cleaned_data_dir
user_inputs_dir = os.path.join(project_dir, user_inputs_dir)
sys.path.append(user_inputs_dir)
from driver_user_inputs import main as get_user_inputs


def main():
    
    action = "clean"
    data_source = "files"
    year, chamber, state, district, raw_file_name = get_user_inputs(data_source = data_source, action = action)
    state = state[0]
    candidate_info = raw_file_name.split("_")[:6]
    _, _, _, last_name, first_name, party = candidate_info

    data = load_raw_file(year = year, chamber = chamber, state = state, district = district, raw_data_dir = raw_data_dir, raw_file_name = raw_file_name)
    data = inject_candidate_info(data = data, state = state, district = district, last_name = last_name, first_name = first_name, party = party)
    data = convert_addresses_to_coordinates(data = data)
    data = arrange_columns(data = data)
    save_cleaned_file(data = data, raw_file_name = raw_file_name, cleaned_data_dir = cleaned_data_dir, year = year, chamber = chamber, state = state, district = district)


if __name__ == "__main__":
    main()