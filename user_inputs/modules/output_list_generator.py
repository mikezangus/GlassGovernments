from .choices_generator import generate_year_choices, generate_chamber_choices, generate_state_choices, generate_district_choices, generate_candidate_choices
from .input_receiver import input_year, input_chamber, input_state, input_district, input_candidate
from .input_processor import process_year_list, process_chamber_input, process_state_input, process_district_input, process_candidate_output


def output_year_list(action: str, source: str, raw_data_dir: str):
    year_choices = generate_year_choices(source, raw_data_dir)
    year_input = input_year(action, year_choices)
    year_output_list = process_year_list(year_input, year_choices)
    return year_output_list


def output_chamber_list(action: str):
    chamber_choices = generate_chamber_choices()
    chamber_input = input_chamber(action, chamber_choices)
    chamber_output_list = process_chamber_input(chamber_input, chamber_choices)
    return chamber_output_list


def output_state_list(action: str, source: str, raw_data_dir: str, year: str, chamber: str):
    state_choices = generate_state_choices(source, raw_data_dir, year, chamber)
    state_input = input_state(action, state_choices)
    state_output_list = process_state_input(state_input, state_choices)
    return state_output_list


def output_district_list(action: str, source: str, raw_data_dir: str, year: str, chamber: str, state: str):
    district_choices = generate_district_choices(source, raw_data_dir, year, chamber, state)
    district_input = input_district(action, district_choices)
    district_output_list = process_district_input(district_input, district_choices)
    return district_output_list


def output_candidate_list(action: str, source: str, raw_data_dir: str, year: str, chamber: str, state: str, district: str = None):
    candidate_choices = generate_candidate_choices(source, raw_data_dir, year, chamber, state, district)
    candidate_input = input_candidate(action, candidate_choices)
    candidate_output_list = process_candidate_output(candidate_input, candidate_choices)
    return candidate_output_list