import json
import sys
from pathlib import Path

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_states_all_file_path


def load_usa_state_codes() -> list:
    path = get_states_all_file_path()
    with open(path, "r") as f:
        codes_json = json.load(f)
    codes = list(codes_json.values())
    return codes