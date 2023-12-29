import os
import sys
from utilities_user_inputs import input_choice, print_retry_message, is_valid_input
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from project_directories import raw_data_dir


def decide_year(data_source: str, action: str):
    subject = "year"
    if data_source.lower() == "internet":
        year_input = input_choice(subject = subject, action = action)
        return year_input
    elif data_source.lower() == "files":
        year_list = sorted([y for y in os.listdir(raw_data_dir) if not y.startswith(".")])
        while True:
            year_input = input_choice(subject = subject, action = action, choices = year_list)
            if year_input in year_list:
                return year_input
            print_retry_message(subject = subject)
            continue
                

def decide_chamber(action: str, chamber_list: list):
    subject = "chamber"
    while True:
        chamber_list = [chamber.capitalize() for chamber in chamber_list]
        chamber_input = input_choice(subject = subject, action = action, choices = chamber_list).capitalize()
        if is_valid_input(choice = chamber_input, choices = chamber_list):
            return chamber_input
        print_retry_message(subject = subject)
        continue         


def decide_state(data_source: str, action: str, year: str = None, chamber: str = None, us_states_all_list: list = None, note = None):
    subject = "state"
    if data_source.lower() == "internet":
        state_input = input_choice(subject = subject, action = action, choices = us_states_all_list, notes = note).upper()
        return state_input
    elif data_source.lower() == "files":
        states_dir = os.path.join(raw_data_dir, year, chamber)
        all_state_dirs = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
        while True:
            state_input = input_choice(subject = subject, action = action, choices = all_state_dirs).upper()
            if is_valid_input(choice = state_input, choices = all_state_dirs):
                return state_input
            print_retry_message(subject = subject)
            continue


def decide_district(data_source: str, action: str, year: str, state: str, chamber: str = None, note = None):
    subject = f"{state} district"
    if data_source.lower() == "internet":
        district_input = input_choice(subject = subject, action = action, notes = note)
        return district_input
    elif data_source.lower() == "files":
        districts_dir = os.path.join(raw_data_dir, year, chamber, state)
        district_list = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        while True:
            district_input = input_choice(subject = subject, action = action, choices = district_list, note = note)
            return district_input
    

def decide_candidate(action: str, year: str, chamber: str, state: str, district: str):
    subject = f"{state}-{district} candidate"
    candidates_dir = os.path.join(raw_data_dir, year, chamber, state, district)
    candidate_list = sorted([file for file in os.listdir(candidates_dir) if not file.startswith(".") and file.endswith(".csv") and file.count("_") == 6])
    candidate_last_names = [file.split("_")[3] for file in candidate_list]
    while True:
        candidate_input = input_choice(subject = subject, action = action, choices = candidate_last_names).upper()
        if candidate_input == "ALL":
            candidate_input = candidate_list
            return candidate_input
        else:
            for file_name in candidate_list:
                if file_name.split("_")[3].upper() == candidate_input:
                    candidate_input = [file_name]
                    return candidate_input
        print_retry_message(subject = subject)  
        continue