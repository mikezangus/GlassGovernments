from .utilities_user_inputs import input_choice, load_commands


def input_year_str(action: str, year_choices: list):
    year_input_str = input_choice(action, "year", year_choices)
    return year_input_str


def input_chamber_str(action: str, chamber_choices: list):
    chamber_input_str = input_choice(action, "chamber", chamber_choices).lower()
    return chamber_input_str


def input_state_str(action: str, state_choices: list):
    commands = load_commands("state")
    state_input_str = input_choice(action, "state", state_choices, commands).upper()
    return state_input_str

def input_house_district_str(action: str, source: str, district_choices: list):
    commands = load_commands("district")
    if source.lower() == "internet":
        district_choices = None
    district_input_str = input_choice(action, "district", district_choices, commands)
    return district_input_str


def input_candidate_str(action: str, candidate_choices: list):
    commands = load_commands("candidate")
    candidate_input_str = input_choice(action, "candidate", candidate_choices, commands).upper()
    return candidate_input_str