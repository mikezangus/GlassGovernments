import json
import os
from pymongo import MongoClient


def load_db(project_dir):
    with open(os.path.join(project_dir, "config.json"), "r") as config_file: config = json.load(config_file)
    config["uri"] = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
    client = MongoClient(config["uri"])
    db = client[config["mongoDatabase"]]
    print("Successfully pinged database")
    return db