import json
import os
from pymongo import MongoClient


def connect_to_mongo_db(subject):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_uploading_path = os.path.dirname(current_dir)
    project_dir = os.path.dirname(data_uploading_path)
    with open(os.path.join(project_dir, "config.json"), "r") as config_file: config = json.load(config_file)
    config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
    client = MongoClient(config["uri"])
    db = client[config["mongoDatabase"]]
    print(f"\n{subject} | Successfully connected to MongoDB")
    return db