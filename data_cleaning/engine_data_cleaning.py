from modules.raw_file_loader import load_raw_file
from modules.candidate_info_injector import inject_candidate_info
from modules.address_converter import convert_addresses_to_coordinates
from modules.column_arranger import arrange_columns
from modules.cleaned_file_saver import save_cleaned_file


def clean_one_candidate(raw_file_name: str, year: str, chamber: str, state: str, district: str, raw_data_dir, cleaned_data_dir):
    candidate_info = raw_file_name.split("_")[:6]
    _, _, _, last_name, first_name, party = candidate_info
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    data = load_raw_file(year = year, chamber = chamber, state = state, district = district, raw_data_dir = raw_data_dir, raw_file_name = raw_file_name)
    data = inject_candidate_info(data = data, state = state, district = district, last_name = last_name, first_name = first_name, party = party)
    data = convert_addresses_to_coordinates(data, subject)
    data = arrange_columns(data = data)
    save_cleaned_file(data = data, raw_file_name = raw_file_name, cleaned_data_dir = cleaned_data_dir, year = year, chamber = chamber, state = state, district = district)