import json
import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.directories import get_config_file_path


def get_mongo_config() -> tuple[str, str]:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = config["mongoUri"]
    db_name = config["mongoDb"]
    return uri, db_name
