import json
import os
import pandas as pd
import requests
import time

base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"
data_directory = os.path.join(base_directory, "data")
source_data_directory = os.path.join(data_directory, "source")
clean_data_directory = os.path.join(data_directory, "clean")

try:
    with open(os.path.join(base_directory, "config.json"), "r") as file:
        config = json.load(file)
        api_key = config["googleMapsApiKey"]
    if not api_key:
        raise ValueError("Google Maps API Key is missing from the config file")
except FileNotFoundError:
    print("Config file not found")
    exit()


def get_coordinates(address, api_key):
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": api_key
    }
    response = requests.get(base_url, params = params)
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "OK":
            latitude = data["results"][0]["geometry"]["location"]["lat"]
            longitude = data["results"][0]["geometry"]["location"]["lng"]
            return [latitude, longitude]
    return None


def clean_data(filename, input_path):
    candidate_info = filename.split("_")
    year, state, district, last_name, first_name, party = candidate_info[:6]
    print(f"Starting to clean {year} {state}-{district} candidate {first_name} {last_name}'s data")

    relevant_columns = [
        "transaction_id",
        "entity_type_desc",
        "contributor_street_1",
        "contributor_city",
        "contributor_state",
        "contributor_zip",
        "contribution_receipt_date",
        "contribution_receipt_amount",
        "candidate_name",
        "candidate_office_full",
        "candidate_office_state",
        "candidate_office_district",
        "donor_committee_name",
        "fec_election_type_desc",
        "fec_election_year"
    ]

    data = pd.read_csv(filepath_or_buffer = input_path, sep = ",", usecols = relevant_columns)

    data["candidate_last_name"] = last_name
    data["candidate_first_name"] = first_name
    data["candidate_state"] = state
    data["candidate_district"] = str(district)
    data["candidate_party"] = party

    data["transaction_id"] = data["transaction_id"].astype(str)
    data["contributor_zip"] = data["contributor_zip"].astype(str)
    data["candidate_office_district"] = data["candidate_office_district"].apply(lambda x: str(int(x)) if not pd.isna(x) else x)
    data["fec_election_year"] = data["fec_election_year"].fillna(0).astype(int).astype(str)
    data = data.loc[data["fec_election_year"] == year]
    data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
    data["contribution_receipt_date"] = pd.to_datetime(data["contribution_receipt_date"], errors = "coerce")
    data["contribution_receipt_date"] = data["contribution_receipt_date"].dt.strftime("%Y-%m-%d")

    data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"]
    address_count = len(data["full_address"])
    start_time = time.time()
    print(f"Converting {address_count} addresses to coordinates, starting at {time.strftime('%H:%M:%S', time.localtime(start_time))}...")
    data["contributor_location"] = data.apply(lambda row: get_coordinates(row["full_address"], api_key), axis = 1)
    end_time = time.time()
    total_time = round((end_time - start_time) / 60, 4)
    print(f"Finished converting {address_count} addresses to coordinates in {total_time:.2f} minutes at a rate of {(address_count / total_time):.2f} addresses per minute")
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
        "contributor_location",
        "fec_election_type_desc",
        "donor_committee_name",
        "candidate_office_full",
        "candidate_office_state",
        "candidate_office_district"
    ]

    data = data.reindex(columns = column_order)
    return data


def save_cleaned_data(district_paths):
    for district_path in district_paths:
        for filename in os.listdir(district_path):
            if filename.startswith("."): 
                continue
            input_path = os.path.join(district_path, filename)
            clean_district_path = district_path.replace(source_data_directory, clean_data_directory)
            output_filename = filename.replace("_source.csv", "_clean.csv")
            output_path = os.path.join(clean_district_path, output_filename)
            if os.path.exists(output_path):
                continue
            cleaned_data = clean_data(filename, input_path)
            os.makedirs(clean_district_path, exist_ok = True)
            cleaned_data.to_csv(path_or_buf = output_path, index = False)
            print(f"Cleaned data saved to {output_path}")


def process_district_data(year, state, district_choice):
    if district_choice == "all":
        all_districts = sorted([d for d in os.listdir(os.path.join(source_data_directory, str(year), state)) if os.path.isdir(os.path.join(source_data_directory, str(year), state, d))], key = lambda x: int(x) if x.isdigit() else 0)
        for district in all_districts:
            district_path = os.path.join(source_data_directory, str(year), state, district)
            save_cleaned_data([district_path])
    else:
        district_path = os.path.join(source_data_directory, str(year), state, district_choice)
        save_cleaned_data([district_path])


if __name__ == "__main__":
    year = "2022"
    state = input("From which state do you want to clean data?: ").upper()
    district_choice = input(f"From which {state} district do you want to clean data?\nTo process one district, enter the district's number, or to process all of {state}'s districts, enter 'all': ")
    process_district_data(year, state, district_choice)
    print("Data cleaning completed")