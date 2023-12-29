import os
import sys
from engine_user_inputs import decide_year, decide_chamber, decide_state, decide_district, decide_candidate
from utilities_user_inputs import load_commands

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import us_states_dir
sys.path.append(us_states_dir)
from us_state_loader import load_states


def year_flow(data_source: str, action: str):
    year_input = decide_year(data_source, action)
    return year_input


def chamber_flow(action: str):
    chamber_list = ["house", "senate"]
    chamber_input = decide_chamber(action, chamber_list).lower()
    if "all" in chamber_input or "both" in chamber_input:
        chamber_input = [chamber for chamber in chamber_list]
    else:
        chamber_input = [chamber_input]
    return chamber_input


def state_flow(data_source: str, action: str, year: str, chamber_list: list):
    subject = "state"
    us_states_all_list, _ = load_states()
    if len(chamber_list) > 1:
        state_input = us_states_all_list
    else:
        chamber = chamber_list[0]
        commands = load_commands(subject = subject)
        note = f"Use one of these commands to format your entry:\n" + "\n".join(commands)
        state_input = decide_state(data_source, action, year, chamber, us_states_all_list, note).upper()
        if "ALL BUT" in state_input:
            excluded_states = state_input[7:].replace(" ", "").split(",")
            excluded_states = [state.strip().upper() for state in excluded_states]
            state_input = [state for state in us_states_all_list if state not in excluded_states]
        elif "ALL STARTING FROM" in state_input:
            state_input_split = state_input.split(" ")
            start_state = state_input_split[-1]
            if start_state in us_states_all_list:
                start_index = us_states_all_list.index(start_state)
                state_input = us_states_all_list[start_index:]
        elif "ALL FROM" in state_input:
            state_input_split = state_input.split(" ")
            start_state = state_input_split[2]
            end_state = state_input_split[-1]
            if start_state and end_state in us_states_all_list:
                start_index = us_states_all_list.index(start_state)
                end_index = us_states_all_list.index(end_state) + 1
                state_input = us_states_all_list[start_index:end_index]
        elif state_input == "ALL":
            state_input = us_states_all_list
        elif "," in state_input:
            state_input = state_input.replace(" ", "").split(",")
            state_input = [state.strip().upper() for state in state_input]
        else:
            state_input = [state_input]
    return state_input
    

def district_flow(data_source: str, action: str, year: str, chamber_list: list, state_list: list):
    subject = "district"
    _, us_states_at_large = load_states()
    if "senate" in chamber_list:
        district_input = ["senate"]
    elif len(state_list) > 1:
        district_input = [str(i).zfill(2) for i in range(1, 100)]
    else:
        chamber = chamber_list[0]
        state = state_list[0]
    if state in us_states_at_large:
        district_input = ["00"]
    else:
        all_possible_districts = [str(i).zfill(2) for i in range(1, 100)]
        commands = load_commands(subject = subject)
        note = f"Use one of these commands to format your entry:\n" + "\n".join(commands)
        district_input = decide_district(data_source, action, year, state, chamber, note).lower()
        if "all but" in district_input:
            excluded_districts = district_input[7:].replace(" ", "").split(",")
            excluded_districts = [district.strip() for district in excluded_districts]
            district_input = [district for district in all_possible_districts if district not in excluded_districts]
        elif "all starting from" in district_input:
            start_district = int(district_input.split()[-1])
            return [str(i).zfill(2) for i in range(start_district, 100)]
        elif "all from" in district_input:
            start_district = int(district_input.split()[2])
            end_district = int(district_input.split()[4])
            district_input = [str(i).zfill(2) for i in range(start_district, end_district + 1)]
        elif "all" in district_input:
            district_input = all_possible_districts
        elif "," in district_input:
            district_input = district_input.replace(" ", "").split(",")
            district_input = [district.strip() for district in district_input]
        else:
            district_input = [district_input]
    return district_input


def candidate_flow(action: str, year: str, chamber_list: list, state_list: list, district_list: list):
    chamber = chamber_list[0]
    state = state_list[0]
    district = district_list[0]
    candidate_input = decide_candidate(action, year, chamber, state, district)
    return candidate_input