import json
import os
import pandas as pd
from pymongo import GEOSPHERE, MongoClient, UpdateOne

base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
clean_dir = os.path.join(data_dir, "clean")

with open(os.path.join(base_dir, "config.json"), "r") as file:
    config = json.load(file)
config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"

client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]

def get_user_choices():
    years = sorted([y for y in os.listdir(clean_dir) if not y.startswith(".")])
    year = input(f"From which year do you want to upload data?:\n{years}\n> ")
    states = sorted([s for s in os.listdir(os.path.join(clean_dir, year)) if not s.startswith(".")])
    state = input(f"From which state do you want to upload data?:\n{states}\n> ").upper()
    districts = ["all"] + sorted([d for d in os.listdir(os.path.join(clean_dir, year, state)) if not d.startswith(".")])
    district = input(f"From which {state} district do you want to upload data?:\n{districts}\n> ")
    candidate = "all"
    if district != "all":
        district_path = os.path.join(clean_dir, year, state, district)
        candidate_files = [f for f in os.listdir(district_path) if f.endswith("_clean.csv")]
        candidates = ["all"] + [f.split('_')[3] for f in candidate_files]
        candidate = input(f"Which candidate do you want to upload?:\n{candidates}\n> ")
    return year, state, district, candidate


def process_upload(upload_path, db):
    try:
        data = pd.read_csv(upload_path, dtype = str)
        data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
        data["contribution_location"] = data["contribution_location"].apply(
            lambda x: {"type": "Point", "coordinates": [float(coord) for coord in x.strip("[]").split(", ")[::-1]]} if isinstance(x, str) else None)
        file_parts = os.path.basename(upload_path).split("_")
        year = file_parts[0]
        chamber = "senate" if "sen" in file_parts[2].lower() else "house"
        name = file_parts[3]
        collection_name = f"{year}_{chamber}"
        print(f"Uploading {name}'s file to collection: {collection_name}")
        collection = db[collection_name]
        collection.create_index([("contribution_location", GEOSPHERE)])
        operations = []
        for record in data.to_dict(orient = "records"):
            operations.append(UpdateOne(
                {"transaction_id": record["transaction_id"]},
                {"$setOnInsert": record},
                upsert = True
            ))
        if operations:
            result = collection.bulk_write(operations)
            print(f"Uploaded {result.upserted_count} new donations for {name} to collection {collection_name}")
        else:
            print(f"No new records for {name} to upload")
    except Exception as e:
        print(f"Error occurred while processing {upload_path}: {e}")
    
if __name__ == "__main__":        
    year, state, district, candidate = get_user_choices()
    districts_to_process = [district] if district != "all" else os.listdir(os.path.join(clean_dir, year, state))
    for district in districts_to_process:
        path = os.path.join(clean_dir, year, state, district if district != "all" else "")
        files_to_process = [f for f in os.listdir(path) if f.endswith("_clean.csv") and (candidate == "all" or candidate.lower() in f.lower())]
        for file_name in files_to_process:
            file_path = os.path.join(path, file_name)
            print(f"\nStarting to process file: {file_name}")
            process_upload(file_path, db)
        if candidate == "all":
            print(f"\nFinished uploading {state.upper()}-{district}'s data\n\n{'-' * 50}")
        else:
            print(f"\nFinished uploading {candidate}'s data")