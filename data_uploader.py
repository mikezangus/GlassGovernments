import json
import os
import pandas as pd
from pymongo import MongoClient

base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"

data_directory = os.path.join(base_directory, "data")
clean_directory = os.path.join(data_directory, "clean")
file = input("\nType '1' to upload Deluzio, type '2' to upload DeMarco, type '3' to upload Shaffer: ")
if file == "1":
    upload_filename = "2022_PA_17_DELUZIO_CHRISTOPHER_DEMOCRATIC_clean.csv"
elif file == "2":
    upload_filename = "2022_PA_17_DEMARCO_SAMUEL-III_REPUBLICAN_clean.csv"
elif file == "3":
    upload_filename = "2022_PA_17_SHAFFER_JEREMY_REPUBLICAN_clean.csv"

upload_path = os.path.join(clean_directory, upload_filename)

with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)

config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]

data = pd.read_csv(upload_path, dtype = {
    "transaction_id": str,
    "candidate_district": str,
    "fec_election_year": str,
    "candidate_office_district": str
})
data["contribution_receipt_amount"] = data["contribution_receipt_amount"].astype(float)
data["contributor_location"] = data["contributor_location"].apply(
    lambda coord_string: [float(x) for x in coord_string[1:-1].split(", ")] if isinstance(coord_string, str) else coord_string
)

collection_name = upload_filename[:7]
collection = db[collection_name]

records = data.to_dict(orient = "records")
for record in records:
    collection.update_one(
        {"transaction_id": record["transaction_id"]},
        {"$set": record},
        upsert = True
    )
print(f"Data uploaded to MongoDB collection: {collection_name}")