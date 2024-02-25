import json
import os
import sys

modules_dir = os.path.dirname(__file__)
processing_dir = os.path.dirname(modules_dir)
data_dir = os.path.dirname(processing_dir)
sys.path.append(data_dir)
from directories import get_config_file_path


def get_mongo_uri() -> str:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = config["mongoUri"]
    return uri
