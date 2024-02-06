import json
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
data_dir = str(current_dir.parent)
sys.path.append(data_dir)
from directories import get_config_file_path


def connect_to_mongo() -> str:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.px0sapn.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
    return uri