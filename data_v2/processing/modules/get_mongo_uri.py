import json
import sys
from pathlib import Path

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_config_file_path


def get_mongo_uri() -> str:
    path = get_config_file_path()
    with open(path, "r") as config_file:
        config = json.load(config_file)
    uri = f"mongodb+srv://{config['mongoUsername']}:{config['mongoPassword']}@{config['mongoCluster']}.0xpxdrt.mongodb.net/{config['mongoDatabase']}?retryWrites=true&w=majority"
    return uri
