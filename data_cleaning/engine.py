from modules.raw_file_loader import load_raw_file
from modules.candidate_info_injector import inject_candidate_info
from modules.address_converter import convert_addresses_to_coordinates
from modules.column_arranger import arrange_columns
from modules.cleaned_file_saver import save_cleaned_file


def clean_one_candidate(year: str, chamber: str, state: str, candidate: str, raw_data_dir: str, cleaned_data_dir: str, district: str = None):
    candidate_info = candidate.split("_")[:6]
    _, _, _, last_name, first_name, party = candidate_info
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    data = load_raw_file(year, chamber, state, candidate, raw_data_dir, district)
    data = inject_candidate_info(data, state, last_name, first_name, party, district)
    data = convert_addresses_to_coordinates(data, subject)
    data = arrange_columns(data)
    save_cleaned_file(data, year, chamber, state, candidate, cleaned_data_dir, district)