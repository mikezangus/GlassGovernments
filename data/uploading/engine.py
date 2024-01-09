from modules.data_type_converter import covert_data_types
from modules.data_uploader import upload_data
from modules.input_file_path_constructor import construct_input_file_path
from modules.mongo_db_connector import connect_to_mongo_db


def upload_one_candidate(candidate: str, input_files_dir: str, i: int, candidate_amount: int):

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    input_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name = input_file_name.split("_")[3:5]

    subject = f"[{(i + 1):,}/{candidate_amount:,}] {year} {state}-{district} {first_name} {last_name}"

    db = connect_to_mongo_db(subject)
    input_file_path = construct_input_file_path(input_files_dir, input_file_name, year, chamber, state, district)
    data = covert_data_types(input_file_path)
    upload_data(db, data, subject, year)