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
        years = sorted([y for y in os.listdir(raw_data_dir) if not y.startswith(".")])
        while True:
            year_input = input_choice(subject = subject, action = action, choices = years)
            if year_input in years:
                return year_input
            print_retry_message(subject = subject)
            continue
                

def decide_chamber(action: str, chambers: list):
    subject = "chamber"
    while True:
        chambers = [chamber.capitalize() for chamber in chambers]
        chamber_input = input_choice(subject = subject, action = action, choices = chambers).capitalize()
        if is_valid_input(choice = chamber_input, choices = chambers):
            return chamber_input.lower()
        print_retry_message(subject = subject)
        continue         


def decide_state(data_source: str, action: str, year: str = None, chamber: str = None, us_states_all: list = None, note = None):
    subject = "state"
    if data_source.lower() == "internet":
        all_states = list(us_states_all)
        state_input = input_choice(subject = subject, action = action, choices = all_states, notes = note).upper()
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
        state = state[0]
        districts_dir = os.path.join(raw_data_dir, year, chamber, state)
        districts = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        if len(districts) == 1:
            district_input = districts[0]
            return district_input
        while True:
            district_input = input_choice(subject = subject, action = action, choices = districts, note = note)
            return district_input
    

def decide_candidate(action: str, year: str, chamber: str, state: list, district: list):
    state = state[0]
    subject = f"{state}-{district} candidate"
    print(f"State: {state}, District: {district}")
    candidates_dir = os.path.join(raw_data_dir, year, chamber, state[0], district[0])
    data_source_file_names = sorted([f for f in os.listdir(candidates_dir) if not f.startswith(".") and f.endswith(".csv") and f.count("_") == 6])
    candidate_last_names = [file.split("_")[3] for file in data_source_file_names]
    while True:
        candidate_input = input_choice(subject = subject, action = action, choices = candidate_last_names).upper()
        for file_name in data_source_file_names:
            if file_name.split("_")[3].upper() == candidate_input:
                return file_name
        print_retry_message(subject = subject)  
        continue