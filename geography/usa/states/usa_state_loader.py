import json
import os


def load_states():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "usa_states_all.json"), "r") as usa_states_all_file:
        usa_state_all_list = json.load(usa_states_all_file)
    with open(os.path.join(current_dir, "usa_states_at_large.json"), "r") as usa_states_at_large_file:
        usa_state_at_large_list = json.load(usa_states_at_large_file)
    return usa_state_all_list, usa_state_at_large_list