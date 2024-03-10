import json
import os
from typing import Dict, List, Literal


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


OutputType = Literal[
    "code_list",
    "name_list",
    "dict"
]


def load_all_states(output_type: OutputType) -> List[str] | Dict[str, str]:
    with open(os.path.join(
        CURRENT_DIR,
        "all_states.json"
    ), "r") as file:
        states = json.load(file)
    if output_type == "code_list":
        return list(states.values())
    elif output_type == "name_list":
        return list(states.keys())
    elif output_type == "dict":
        return states


def load_at_large_states(output_type: OutputType) -> List[str] | Dict[str, str]:
    with open(os.path.join(
        CURRENT_DIR,
        "at_large_states.json"
    ), "r") as file:
        states = json.load(file)
    if output_type == "code_list":
        return list(states.values())
    elif output_type == "name_list":
        return list(states.keys())
    elif output_type == "dict":
        return states


def load_states(state_type: Literal["all", "at_large"], output_type: OutputType) -> List[str] | Dict[str, str]:
    if state_type == "all":
        return load_all_states(output_type)
    elif state_type == "at_large":
        return load_at_large_states(output_type)
