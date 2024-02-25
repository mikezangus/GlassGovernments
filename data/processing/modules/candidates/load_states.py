import json
import sys
from pathlib import Path

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_states_all_file_path


def load_states() -> list:
    path = get_states_all_file_path()
    with open(path, "r") as f:
        states_json = json.load(f)
    states = list(states_json.values())
    return states
