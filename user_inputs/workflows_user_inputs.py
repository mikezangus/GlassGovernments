import os
import sys

from modules.output_list_generator import output_year_list, output_chamber_list, output_state_list, output_district_list, output_candidate_list
from engine_user_inputs import process_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from us_states.us_state_loader import load_states
_, us_state_at_large_list = load_states()



def process_multiple_candidates(action: str, year: str, chamber: str, state: str, candidate_list: list, district: str = None):
    for candidate in candidate_list:
        process_one_candidate(action, year, chamber, state, candidate, district)


def process_multiple_districts(action: str, source: str, raw_data_dir: str, year: str, chamber: str, state: str, district_list: list):
    for district in district_list:
        candidate_list = output_candidate_list(action, source, raw_data_dir, year, chamber, state)
        process_multiple_candidates(action, year, chamber, state, candidate_list, district)
    

def process_multiple_states(action: str, source: str, raw_data_dir: str, year: str, chamber: str, state_list: list):
    for state in state_list:
        if chamber.lower() == "house":
            if state in us_state_at_large_list:
                print("at large state")
                candidate_list = output_candidate_list(action, source, raw_data_dir, year, chamber, state, "00")
                process_multiple_candidates(action, year, chamber, state, candidate_list, "00")
            else:
                district_list = output_district_list(action, source, raw_data_dir, year, chamber, state)
                process_multiple_districts(action, source, raw_data_dir, year, chamber, state, district_list)
        elif chamber.lower() == "senate":
            candidate_list = output_candidate_list(action, source, raw_data_dir, year, chamber, state)
            process_multiple_candidates(action, year, chamber, state, candidate_list)
    

def process_multiple_chambers(action: str, source: str, raw_data_dir: str, year: str, chamber_list :list):
    for chamber in chamber_list:
        state_list = output_state_list(action, source, raw_data_dir, year, chamber)
        process_multiple_states(action, source, raw_data_dir, year, chamber, state_list)
    

def process_multiple_years(action: str, source: str, raw_data_dir: str, year_list: list):
    for year in year_list:
        chamber_list = output_chamber_list(action)
        process_multiple_chambers(action, source, raw_data_dir, year, chamber_list)


def determine_workflow(action, source: str, raw_data_dir: str):

    year_list = output_year_list(action, source, raw_data_dir)
    if len(year_list) > 1:
        process_multiple_years(action, year_list)
        return
    else:
        year = year_list[0]
    
    chamber_list = output_chamber_list(action)
    if len(chamber_list) > 1:
        process_multiple_chambers(action, source, raw_data_dir, year, chamber_list)
        return
    else:
        chamber = chamber_list[0]

    state_list = output_state_list(action, source, raw_data_dir, year, chamber)
    if len(state_list) > 1:
        process_multiple_states(action, source, raw_data_dir, year, chamber, state_list)
        return
    else:
        state = state_list[0]
        if state in us_state_at_large_list:
            candidate_list = output_candidate_list(action, source, raw_data_dir, year, chamber, state, "00")
            process_multiple_candidates(action, year, chamber, state, candidate_list, "00")
            return

    district_list = output_district_list(action, source, raw_data_dir, year, chamber, state)
    if len(district_list) > 1:
        process_multiple_districts(action, source, raw_data_dir, year, chamber, state, district_list)
        return
    else:
        district = district_list[0]

    if source.lower() == "files":
        candidate_list = output_candidate_list(action, source, raw_data_dir, year, chamber, state, district)
        if len(candidate_list) > 1:
            process_multiple_candidates(action, year, chamber, state, candidate_list, district)
            return
        else:
            candidate = candidate_list[0]
            process_one_candidate(action, year, chamber, state, candidate, district)
            return