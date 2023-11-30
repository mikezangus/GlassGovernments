import os
import pandas as pd
import requests
import time


base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
src_data_dir = os.path.join(data_dir, "source")


def clean_data(file_name, src_path):

    def get_coordinates(address):
        try:
            base_url = "https://nominatim.openstreetmap.org/search"
            params = { "q": address, "format": "json" }
            response = requests.get(base_url, params = params)
            response.raise_for_status()
            data = response.json()
            if data:
                latitude = float(data[0]["lat"])
                longitude = float(data[0]["lon"])
                return [latitude, longitude]
            return None
        except requests.RequestException as e:
            print(f"Error fetching coordinates: {e}")
            return None
            
    candidate_info = file_name.split("_")
    year, state, district, last_name, first_name, party = candidate_info[:6]

    relevant_cols = [
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

    data = pd.read_csv(filepath_or_buffer = src_path, sep = ",", usecols = relevant_cols)
    data["fec_election_year"] = data["fec_election_year"].fillna(0).astype(int).astype(str)
    data = data.loc[data["fec_election_year"] == year]

    data["candidate_last_name"] = last_name
    data["candidate_first_name"] = first_name
    data["candidate_state"] = state
    data["candidate_district"] = district
    data["candidate_party"] = party

    string_cols = data.columns.drop(['candidate_office_district', 'contribution_receipt_amount'])
    data[string_cols] = data[string_cols].astype(str) 
    
    data["candidate_office_district"] = data["candidate_office_district"].apply(
        lambda x: str(int(x)) if (not pd.isna(x) and x != '' and str(x).isdigit()) else x
    )
    data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)


    data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"]
    address_count = len(data["full_address"])
    start_time = time.time()
    print(f"Converting {address_count} addresses to coordinates, starting at {time.strftime('%H:%M:%S', time.localtime(start_time))}...")
    data["contribution_location"] = data["full_address"].apply(get_coordinates)
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
        "contribution_location",
        "fec_election_type_desc",
        "donor_committee_name",
        "candidate_office_full",
        "candidate_office_state",
        "candidate_office_district"
    ]

    data = data.reindex(columns = column_order)
    return data


def clean_file(year, state, district, candidate_file):
    
    src_file_path = os.path.join(src_data_dir, year, state, district, candidate_file)
    cleaned_data_dir = os.path.join(data_dir, "cleanX")
    cleaned_file_dir = os.path.join(cleaned_data_dir, year, state, district)
    os.makedirs(cleaned_file_dir, exist_ok = True)

    print(f"Starting to clean file: {candidate_file}")
    clean_file = clean_data(file_name = candidate_file, src_path = src_file_path)
    cleaned_file_name = candidate_file.replace("source", "clean")
    cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
    os.path.isfile(cleaned_file_path)

    clean_file.to_csv(path_or_buf = cleaned_file_path, index = False)
    print(f"Finished cleaning file: {cleaned_file_name}\n")
    


def get_user_input():

# 1. Year
    def decide_year():
        years = sorted([y for y in os.listdir(src_data_dir) if not y.startswith(".")])
        year_input = input(str(f"From which year do you want to clean data?:\n{', '.join(years)}\n> "))
        decide_state(year = year_input)

# 2. State
    def decide_state(year):
        states_dir = os.path.join(src_data_dir, year)
        states = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
        state_input = input(f"From which state do you want to clean files? For all states, enter 'all':\n{', '.join(states)}\n> ").upper()
        if state_input == "ALL":
            process_all_states(year = year)
        else:
            decide_district(year = year, state = state_input)

    def process_all_states(year):
        print(f"\nCleaning data from {year} for all states\n{'-' * 100}")
        states_dir = os.path.join(src_data_dir, year)
        states = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
        for state in states:
            process_all_districts(year = year, state = state)

# 3. District
    def decide_district(year, state):
        districts_dir = os.path.join(src_data_dir, year, state)
        districts = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        if len(districts) == 1:
            decide_candidate(year = year, state = state, district = districts[0])   
        else:
            district_input = input(f"From which district do you want to clean files? For all districts, enter 'all':\n{', '.join(districts)}\n> ")
            if district_input.lower() == "all":
                process_all_districts(year = year, state = state)
            else:
                decide_candidate(year = year, state = state, district = district_input)

    def process_all_districts(year, state):
        print(f"\nCleaning data for all {state} districts\n{'-' * 100}")
        districts_dir = os.path.join(src_data_dir, year, state)
        districts = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        for district in districts:
            process_all_candidates(year = year, state = state, district = district)

# 4. Candidate
    def decide_candidate(year, state, district):
        candidates_dir = os.path.join(src_data_dir, year, state, district)
        candidate_files = [f for f in os.listdir(candidates_dir) if not f.startswith(".") and f.count("_") == 6]
        candidate_last_names = [file.split("_")[3] for file in candidate_files]
        candidate_input = input(f"Which candidate's file do you want to clean? For all candidates, enter 'all':\n{', '.join(candidate_last_names)}\n> ").upper()
        if candidate_input == "ALL":
            process_all_candidates(year = year, state = state, district = district)
        else:
            for candidate_file in candidate_files:
                if candidate_file.split("_")[3].upper() == candidate_input:
                    process_one_candidate(year = year, state = state, district = district, candidate = candidate_file)       
    
    def process_all_candidates(year, state, district):
        print(f"\nCleaning data for all {state}-{district} candidates\n{'-' * 75}")
        candidates_dir = os.path.join(src_data_dir, year, state, district)
        candidate_files = [f for f in os.listdir(candidates_dir) if not f.startswith(".") and f.count("_") == 6]
        for candidate_file in candidate_files:
            process_one_candidate(year = year, state = state, district = district, candidate = candidate_file)
    
    def process_one_candidate(year, state, district, candidate):
        clean_file(year = year, state = state, district = district, candidate_file = candidate)


    decide_year()


if __name__ == "__main__":
    get_user_input()
    print(f"Data cleaning completed")