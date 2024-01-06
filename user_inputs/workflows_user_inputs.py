import os
import sys

from .modules.output_list_generator import output_year_list, output_chamber_list, output_state_list, output_house_district_list, output_candidate_list
from .engine_user_inputs import process_multiple_years, process_multiple_chambers, process_multiple_states, process_one_state, process_multiple_districts, process_one_district, process_multiple_candidates, process_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from us_states.us_state_loader import load_states


def determine_workflow_internet(action: str, source: str, year: str, chamber: str, state: str):

    if chamber.lower() == "house":
        district_list = output_house_district_list(action, source, year, chamber, state)
        if len(district_list) > 1:
            output_list_districts = process_multiple_districts([], source, year, chamber, state, district_list)
            return output_list_districts
        district = district_list[0]
        output_list_district = process_one_district([], source, year, chamber, state, district)
        return output_list_district
    
    elif chamber.lower() == "senate":
        output_list_state = process_one_state([], source, year, chamber, state)
        return output_list_state


def determine_workflow_files(action: str, source: str, year: str, chamber: str, state: str, data_dir: str):

    if chamber.lower() == "house":
        _, us_state_at_large_list = load_states()
        if state in us_state_at_large_list:
            district_list = ["00"]
        else:
            district_list = output_house_district_list(action, source, year, chamber, state, data_dir)
        if len(district_list) > 1:
            output_list_districts = process_multiple_districts([], source, year, chamber, state, district_list, data_dir)
            return output_list_districts
        district = district_list[0]

        candidate_list = output_candidate_list(action, year, chamber, state, data_dir, district)
        if len(candidate_list) > 1:
            output_list_candidates = process_multiple_candidates([], year, chamber, state, district, candidate_list, data_dir)
            return output_list_candidates
        candidate = candidate_list[0]
        output_candidate = [process_one_candidate(year, chamber, state, district, candidate)]
        return output_candidate
    
    elif chamber.lower() == "senate":
        candidate_list = output_candidate_list(action, year, chamber, state, data_dir)
        if len(candidate_list) > 1:
            output_list_candidates = process_multiple_candidates([], year, chamber, state, candidate_list = candidate_list, data_dir = data_dir)
            return output_list_candidates
        candidate = candidate_list[0]
        output_candidate = [process_one_candidate(year, chamber, state, candidate = candidate)]
        return output_candidate
    

def determine_workflow(action: str, source: str, data_dir: str = None):
     
    year_list = output_year_list(action, source, data_dir)
    if len(year_list) > 1:
        output_list = process_multiple_years([], source, year_list, data_dir)
        return output_list
    year = year_list[0]

    chamber_list = output_chamber_list(action)
    if len(chamber_list) > 1:
        output_list = process_multiple_chambers([], source, year, chamber_list, data_dir)
        return output_list
    chamber = chamber_list[0].upper()

    state_list = output_state_list(action, source, year, chamber, data_dir)
    if len(state_list) > 1:
        output_list = process_multiple_states([], source, year, chamber, state_list, data_dir)
        return output_list
    state = state_list[0]

    if source.lower() == "internet":
        output_list = determine_workflow_internet(action, source, year, chamber, state)
    elif source.lower() == "files":
        output_list = determine_workflow_files(action, source, year, chamber, state, data_dir)
    return output_list