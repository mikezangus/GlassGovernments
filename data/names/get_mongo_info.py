import json
import os
import sys

names_dir = os.path.dirname(__file__)
data_dir = os.path.dirname(names_dir)
sys.path.append(data_dir)
from directories import get_config_file_path


def get_mongo_info() -> tuple[str, str]:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = config["mongoUri"]
    db = config["mongoDb"]
    return uri, db
