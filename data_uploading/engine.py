from modules.mongo_db_connector import connect_to_mongo_db
from modules.cleaned_file_path_constructor import construct_cleaned_file_path
from modules.data_type_converter import covert_data_types
from modules.data_uploader import upload_data


def upload_one_candidate(candidate: str, cleaned_data_dir: str):

    split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
    constituency = candidate[:split_index]
    cleaned_file_name = candidate[split_index + 1:]
    year, chamber, state, district = constituency.split("_")
    last_name, first_name = cleaned_file_name.split("_")[3:5]

    subject = f"{year} {state}-{district} {first_name} {last_name}"

    db = connect_to_mongo_db(subject)
    cleaned_file_path = construct_cleaned_file_path(cleaned_data_dir, cleaned_file_name, year, chamber, state, district)
    data = covert_data_types(cleaned_file_path)
    upload_data(db, data, subject, year, chamber)