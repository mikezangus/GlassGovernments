import os
import pandas as pd
import requests
import time
from user_inputs import get_user_input


base_dir = os.path.dirname(os.path.abspath(__file__))
data_base_dir = os.path.join(base_dir, "data")
src_data_dir = os.path.join(data_base_dir, "source")


def clean_data(src_file_name, src_file_path):

    def get_coordinates(address):
        try:
            base_url = "https://nominatim.openstreetmap.org/search"
            params = { "q": address, "format": "json" }
            response = requests.get(url = base_url, params = params)
            response.raise_for_status()
            data = response.json()
            if data:
                latitude = float(data[0]["lat"])
                longitude = float(data[0]["lon"])
                return f"[{latitude}, {longitude}]"
            return None
        except requests.RequestException as e:
            print(f"Error fetching coordinates: {e}")
            return None
            
    candidate_info = src_file_name.split("_")
    year, state, district, last_name, first_name, party = candidate_info[:6]

    relevant_cols = [
        "transaction_id",
        "entity_type_desc",
        "contributor_street_1", "contributor_city", "contributor_state", "contributor_zip",
        "contribution_receipt_date", "contribution_receipt_amount",
        "candidate_name", "candidate_office_full", "candidate_office_state", "candidate_office_district",
        "donor_committee_name",
        "fec_election_type_desc", "fec_election_year"
    ]

    data = pd.read_csv(
        filepath_or_buffer = src_file_path, sep = ",", usecols = relevant_cols, na_values = "", keep_default_na = False, low_memory = False
    )

    data["fec_election_year"] = data["fec_election_year"].fillna(0).astype(int).astype(str)
    data = data.loc[data["fec_election_year"] == year]

    data["candidate_state"] = state
    data["candidate_district"] = district
    data["candidate_last_name"] = last_name
    data["candidate_first_name"] = first_name
    data["candidate_party"] = party

    string_cols = data.columns.drop(["candidate_office_district"])
    data[string_cols] = data[string_cols].astype(str) 
    
    data["candidate_office_district"] = data["candidate_office_district"].apply(
        lambda x: str(int(x)) if (not pd.isna(x) and x != '' and str(x).isdigit()) else x
    )
    data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"]
    total_address_count = len(data["full_address"])

    start_time = time.time()
    print(f"{' ' * 9}Starting to convert {format(total_address_count, ',')} addresses to coordinates. Current time: {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    last_update_time = start_time
    converted_count = 0
    for idx, address in enumerate(data["full_address"]):
        data.at[idx, "contribution_location"] = get_coordinates(address)
        converted_count += 1
        if time.time() - last_update_time >= 300:
            loop_elapsed_time = (time.time() - start_time) / 60 
            loop_conversion_percentage = converted_count / total_address_count * 100
            loop_conversion_rate = converted_count / loop_elapsed_time
            projected_total_time = total_address_count / loop_conversion_rate
            projected_total_remaining_time = projected_total_time - loop_elapsed_time
            projected_total_end_time = time.strftime('%H:%M:%S', time.localtime(start_time + projected_total_time * 60))
            loop_current_minute = f"Minute {int(loop_elapsed_time)}: "
            print(f"{' ' * 9}{loop_current_minute}Converted {format(converted_count, ',')} of {format(total_address_count, ',')} addresses at {int(loop_conversion_rate)} addresses per minute")
            print(f"{' ' * (9 + len(loop_current_minute))}{loop_conversion_percentage:.1f}% complete, projected to complete in {projected_total_remaining_time:.1f} minutes at {projected_total_end_time}")
            last_update_time = time.time()
    
    end_time = time.time()
    total_time = (end_time - start_time) / 60
    total_conversion_rate = total_address_count / total_time
    print(f"Finished converting {format(total_address_count, ',')} addresses to coordinates in {total_time:.2f} minutes at {total_conversion_rate:.2f} addresses per minute")
    data.drop(columns = ["contributor_street_1", "contributor_city", "contributor_state", "contributor_zip", "full_address"], inplace = True)

    column_order = [
        "transaction_id",
        "candidate_last_name",
        "candidate_first_name",
        "fec_election_year",
        "candidate_state",
        "candidate_district",
        "candidate_party",
        "contribution_receipt_date",
        "contribution_receipt_amount",
        "entity_type_desc",
        "contribution_location",
        "fec_election_type_desc",
        "donor_committee_name",
        "candidate_office_full",
        "candidate_office_state",
        "candidate_office_district"
    ]

    data = data.reindex(columns = column_order)
    return data


def save_cleaned_file(year, state, district, src_file_name):
    
    src_file_path = os.path.join(src_data_dir, year, state, district, src_file_name)
    cleaned_data_dir = os.path.join(data_base_dir, "cleanX")
    cleaned_file_dir = os.path.join(cleaned_data_dir, year, state, district)
    os.makedirs(cleaned_file_dir, exist_ok = True)

    print(f"Starting to clean file: {src_file_name}")
    clean_file = clean_data(src_file_name = src_file_name, src_file_path = src_file_path)
    cleaned_file_name = src_file_name.replace("source", "clean")
    cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    os.path.isfile(cleaned_file_path)

    clean_file.to_csv(path_or_buf = cleaned_file_path, index = False)
    print(f"Finished cleaning file: {cleaned_file_name}\n")


if __name__ == "__main__":
    get_user_input(callback = save_cleaned_file, data_dir = src_data_dir)
    print(f"Data cleaning completed")