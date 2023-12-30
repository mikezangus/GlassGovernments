from .choices_generator import generate_year_choices, generate_chamber_choices, generate_state_choices, generate_district_choices, generate_candidate_choices
from .utilities_user_inputs import input_choice, load_commands


def input_year(action: str, year_choices: list):
    year_input = input_choice("year", action, year_choices)
    return year_input


def input_chamber(action: str, chamber_choices: list):
    chamber_input = input_choice("chamber", action, chamber_choices).lower()
    return chamber_input


def input_state(action: str, state_choices: list):
    subject = "state"
    commands = load_commands(subject)
    state_input = input_choice(subject, action, state_choices, commands).upper()
    return state_input

def input_district(action: str, district_choices: list):
    subject = "state"
    commands = load_commands(subject)
    district_input = input_choice(subject, action, district_choices, commands)
    return district_input


def input_candidate(action: str, candidate_choices: list):
    subject = "candidate"
    commands = load_commands(subject)
    candidate_input = input_choice(subject, action, candidate_choices, commands).upper()
    return candidate_input