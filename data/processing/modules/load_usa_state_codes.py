import json
import sys
from pathlib import Path

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_usa_states_all_file_path


def load_usa_state_codes() -> list:
    path = get_usa_states_all_file_path()
    with open(path, "r") as f:
        usa_state_codes = json.load(f)
    usa_state_codes = list(usa_state_codes.values())
    return usa_state_codes