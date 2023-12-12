import json
import os
import pandas as pd
from pymongo import GEOSPHERE, MongoClient, UpdateOne
from user_inputs import get_user_inputs
from directories import current_path, cleaned_data_dir


with open(os.path.join(current_path, "config.json"), "r") as config_file: config = json.load(config_file)
config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]


def prepare_data_for_upload(cleaned_file_path):
    data = pd.read_csv(filepath_or_buffer = cleaned_file_path, sep = ",")
    data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
    data["contribution_location"] = data["contribution_location"].apply(
        lambda x: {"type": "Point", "coordinates": [float(coord) for coord in x.strip("[]").split(", ")[::-1]]} if isinstance(x, str) else None)
    return data


def upload_data(year, state, district, file_name):
    candidate_info = file_name.split("_")
    first_name, last_name = candidate_info[4], candidate_info[3]
    cleaned_file_path = os.path.join(cleaned_data_dir, year, state, district, file_name)
    data = prepare_data_for_upload(cleaned_file_path = cleaned_file_path)
    chamber = "senate" if "sen" in district.lower() else "house"
    collection_name = f"{year}_{chamber}x"
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
        print(f"Uploaded {result.upserted_count} new donations for {first_name} {last_name} to {collection_name}")
    else:
        print(f"No new records for {first_name} {last_name} to upload")


if __name__ == "__main__":
    get_user_inputs(chamber = False, action = "upload", data_dir = cleaned_data_dir, callback = upload_data)
    print("\nFinished uploading data")