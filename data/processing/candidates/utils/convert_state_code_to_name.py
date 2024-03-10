import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CANDIDATES_DIR = os.path.dirname(CURRENT_DIR)
PROCESSING_DIR = os.path.dirname(CANDIDATES_DIR)
DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from geography.usa.states.load_states import load_states



def convert_state_code_to_name(state_code: str) -> str:
    states_dict = load_states("all", "dict")
    inverse_states_dict = {
        v: k for k, v in states_dict.items()
    }
    return inverse_states_dict.get(state_code, "")
