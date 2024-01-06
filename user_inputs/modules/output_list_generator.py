from .choices_generator import generate_year_choices, generate_chamber_choices, generate_state_choices, generate_house_district_choices, generate_candidate_choices
from .input_str_receiver import input_year_str, input_chamber_str, input_state_str, input_house_district_str, input_candidate_str
from .input_list_processor import process_year_input_str, process_chamber_input_str, process_state_input_str, process_house_district_input_str, process_candidate_output_str


def output_year_list(action: str, source: str, data_dir: str = None):
    year_choices_list = generate_year_choices(source, data_dir)
    year_input_str = input_year_str(action, year_choices_list)
    year_output_list = process_year_input_str(year_input_str, year_choices_list)
    return year_output_list


def output_chamber_list(action: str):
    chamber_choices_list = generate_chamber_choices()
    chamber_input_str = input_chamber_str(action, chamber_choices_list)
    chamber_output_list = process_chamber_input_str(chamber_input_str, chamber_choices_list)
    return chamber_output_list


def output_state_list(action: str, source: str, year: str, chamber: str, data_dir: str = None):
    state_choices_list = generate_state_choices(source, year, chamber, data_dir)
    state_input_str = input_state_str(action, state_choices_list)
    state_output_list = process_state_input_str(state_input_str, state_choices_list)
    return state_output_list


def output_house_district_list(action: str, source: str, year: str, chamber: str, state: str, data_dir: str = None):
    district_choices_list = generate_house_district_choices(source, year, chamber, state, data_dir)
    district_input_str = input_house_district_str(action, source, district_choices_list)
    district_output_list = process_house_district_input_str(district_input_str, district_choices_list)
    return district_output_list


def output_candidate_list(action: str, year: str, chamber: str, state: str, data_dir: str, district: str = None):
    candidate_choices_list = generate_candidate_choices(year, chamber, state, data_dir, district)
    candidate_input_str = input_candidate_str(action, candidate_choices_list)
    candidate_output_list = process_candidate_output_str(candidate_input_str, candidate_choices_list)
    return candidate_output_list