from .modules.choices_generator import generate_chamber_choices, generate_state_choices, generate_district_choices, generate_candidate_choices
from us_states.us_state_loader import load_states


def process_one_candidate(year: str, chamber: str, state: str, district: str = None, candidate: str = None):
    if not district:
        district = chamber.upper()
    output_str = f"{year}_{chamber}_{state}_{district}_{candidate}"
    return output_str


def process_multiple_candidates(output_list: list, year: str, chamber: str, state: str, district: str = None, candidate_list: list = None, raw_data_dir: str = None):
    if not candidate_list:
        candidate_list = generate_candidate_choices(year, chamber, state, raw_data_dir, district)
    for candidate in candidate_list:
        output_str = process_one_candidate(year, chamber, state, district, candidate)
        output_list.append(output_str)
    return output_list


def process_one_district(output_list: list, source: str, year: str, chamber: str, state: str, district: str, raw_data_dir: str = None):
    if source.lower() == "internet":
        output_str = f"{year}_{chamber}_{state}_{district}"
        output_list.append(output_str)
        return output_list
    elif source.lower() == "files":
        output_list = process_multiple_candidates(output_list, year, chamber, state, district, raw_data_dir = raw_data_dir)
    return output_list


def process_multiple_districts(output_list: list, source: str, year: str, chamber: str, state: str, district_list: list = None, raw_data_dir: str = None):
    if not district_list:
        district_list = generate_district_choices(source, year, chamber, state, raw_data_dir)
    for district in district_list:
        output_list = process_one_district(output_list, source, year, chamber, state, district, raw_data_dir)
    return output_list


def process_one_state(output_list: list, source: str, year: str, chamber: str, state: str, raw_data_dir: str = None):
    if chamber.lower() == "house":
        _, us_state_at_large_list = load_states()
        if state in us_state_at_large_list:
            output_list = process_one_district(output_list, source, year, chamber, state, "00", raw_data_dir)
        else:
            output_list = process_multiple_districts(output_list, source, year, chamber, state, raw_data_dir = raw_data_dir)
    elif chamber.lower() == "senate":
        if source.lower() == "internet":
            output_str = f"{year}_{chamber}_{state}_{chamber}"
            output_list.append(output_str)
        elif source.lower() == "files":
            output_list = process_multiple_candidates(output_list, year, chamber, state, raw_data_dir = raw_data_dir)
    return output_list
    

def process_multiple_states(output_list: list, source: str, year: str, chamber: str, state_list: list = None, raw_data_dir: str = None):
    if not state_list:
        state_list = generate_state_choices(source, year, chamber, raw_data_dir)
    for state in state_list:
        output_list = process_one_state(output_list, source, year, chamber, state, raw_data_dir)
    return output_list


def process_multiple_chambers(output_list: list, source: str, year: str, chamber_list: list = None, raw_data_dir: str = None):
    if not chamber_list:
        chamber_list = generate_chamber_choices()
    for chamber in chamber_list:
        output_list = process_multiple_states(output_list, source, year, chamber, raw_data_dir = raw_data_dir)
    return output_list
    

def process_multiple_years(output_list_init: list, source: str, year_list: list, raw_data_dir: str = None):
    for year in year_list:
        output_list = process_multiple_chambers(output_list_init, source, year, raw_data_dir = raw_data_dir)
    return output_list