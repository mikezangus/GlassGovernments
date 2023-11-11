import json
import os
import pandas as pd
from pymongo import MongoClient

base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"

data_directory = os.path.join(base_directory, "data")
clean_directory = os.path.join(data_directory, "clean")

with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)
config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"

client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]

def get_user_choices():
    year = get_user_choice("Which year's data do you want to upload?: ", os.listdir(clean_directory))
    states = os.listdir(os.path.join(clean_directory, year))
    state = get_user_choice("From which state do you want to upload data?: ", states)
    all_districts = ["all"] + os.listdir(os.path.join(clean_directory, year, state))
    district = get_user_choice(f"From which {state} district do you want to upload data?: ", all_districts)
    district_path = os.path.join(clean_directory, year, state, district) if district != "all" else os.path.join(clean_directory, year, state)
    candidate_files = [f for f in os.listdir(district_path) if f.endswith("_clean.csv")]
    candidates = ["all"] + [f.split('_')[3] for f in candidate_files]
    candidate = get_user_choice("Which candidate do you want to upload?: ", candidates)
    return year, state, district, candidate

def get_user_choice(prompt, available_options):
    print("Available options:", available_options)
    choice = input(prompt).strip()
    while choice.upper() not in [option.upper() for option in available_options]:
        print("Invalid choice. Please choose from the available options.")
        choice = input(prompt).strip()
    return choice.upper()

def process_upload(upload_path, db):
    data = pd.read_csv(upload_path, dtype={
        "transaction_id": str,
        "candidate_district": str,
        "fec_election_year": str,
        "candidate_office_district": str
    })
    data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
    data["contributor_location"] = data["contributor_location"].apply(
        lambda coord_string: [float(x) for x in coord_string[1:-1].split(", ")] if isinstance(coord_string, str) else coord_string
    )
    collection_name = os.path.basename(upload_path)[:7]
    print(f"\nUploading file to collection: {collection_name}")
    collection = db[collection_name]

    records = data.to_dict(orient = "records")
    for record in records:
        collection.update_one(
            {"transaction_id": record["transaction_id"]},
            {"$set": record},
            upsert = True
        )
        

year, state, district, candidate = get_user_choices()

if district == "all":
    districts = os.listdir(os.path.join(clean_directory, year, state))
else:
    districts = [district]

for district in districts:
    path = os.path.join(clean_directory, year, state, district)
    print(f"\nChecking path: {path}")
    all_files = os.listdir(path)
    print(f"\nAll files in directory: {all_files}")
    if candidate == "ALL":
        files = [f for f in all_files if f.endswith("_clean.csv")]
    else:
        files = [f for f in all_files if candidate in f.upper()]

    print(f"\nFiles to be processed: {files}")
    for file in files:
        print(f"\nProcessing file {file}")
        process_upload(os.path.join(path, file), db)
        print(f"\nFinished uploading file {file}")

print("\nFinished uploading data")