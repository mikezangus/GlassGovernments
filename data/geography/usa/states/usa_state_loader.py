import json
import os


def load_full_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "usa_states_all.json"), "r") as usa_states_all_file:
        states_dict = json.load(usa_states_all_file)
        return states_dict


def load_states():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(current_dir, "usa_states_all.json"), "r") as usa_states_all_file:
        usa_states_all_dict = json.load(usa_states_all_file)
        usa_states_all_list = list(usa_states_all_dict.values())
    with open(os.path.join(current_dir, "usa_states_at_large.json"), "r") as usa_states_at_large_file:
        usa_states_at_large_dict = json.load(usa_states_at_large_file)
        usa_states_at_large_list = list(usa_states_at_large_dict.values())
    return usa_states_all_list, usa_states_at_large_list