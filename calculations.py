import json
import os
from pymongo import MongoClient

base_directory = "/Users/zangus/Documents/Projects/Project_CREAM"
with open(os.path.join(base_directory, "config.json"), "r") as file:
    config = json.load(file)

config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"

client = MongoClient(config["uri"])
db = client[config["mongoDatabase"]]
collection = db["2022_PA"]

candidate_last_name = input("\nWhich candidate do you want to calculate?: ").upper()

pipeline = [
    {"$match": {"candidate_last_name": candidate_last_name}},
    {
        "$group": {
            "_id": "$entity_type_desc",
            "total_amount": {"$sum": "$contribution_receipt_amount"}
        }
    },
    {
        "$sort": {"total_amount": -1}
    }
]

results = list(collection.aggregate(pipeline))
total_raised = 0
for result in results:
    entity_type = result["_id"]
    amount = result["total_amount"]
    total_raised += amount
    print(f"Entity type: {entity_type} | Total raised: ${amount:,.2f}")
print(f"Total raised by {candidate_last_name}: ${total_raised:,.2f}")