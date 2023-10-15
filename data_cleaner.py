import json
import os
import pandas as pd
import requests
import time

base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"

data_directory = os.path.join(base_directory, "data")
_2022_PA_17_directory = os.path.join(data_directory, "2022", "PA", "17")
clean_directory = os.path.join(data_directory, "clean")
file = input("\nType '1' to clean Deluzio, type '2' to clean DeMarco, type '3' to clean Shaffer: ")
if file == "1":
    input_filename = "2022_PA_17_DELUZIO_CHRISTOPHER_DEMOCRATIC_source.csv"
elif file == "2":
    input_filename = "2022_PA_17_DEMARCO_SAMUEL-III_REPUBLICAN_source.csv"
elif file == "3":
    input_filename = "2022_PA_17_SHAFFER_JEREMY_REPUBLICAN_source.csv"

input_path = os.path.join(_2022_PA_17_directory, input_filename)

with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)
api_key = config["googleMapsApiKey"]

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

candidate_info = input_filename.split("_")
year, state, district, last_name, first_name, party = candidate_info[:6]

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
data = data.query("fec_election_year == @year")
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
print(f"Finished converting {address_count} addresses to coordinates in {total_time} minutes at a rate of {(address_count / total_time):.2f} addresses per minute")
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
output_filename = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_clean.csv"
output_path = os.path.join(clean_directory, output_filename)
data.to_csv(path_or_buf = output_path, index = False)
print(f"Cleaned data saved to {output_path}")