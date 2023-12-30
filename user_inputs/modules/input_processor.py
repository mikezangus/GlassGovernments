def process_year_list(year_input: str, year_choices: list):
    if "all" in year_input.lower():
        year_input_list = year_choices
    elif "," in year_input:
        year_input_split = year_input.replace(" ", "").split(",")
        year_input_list = [y.strip() for y in year_input_split]
    else:
        year_input_list = [year_input]
    return year_input_list


def process_chamber_input(chamber_input: str, chamber_choices: list):
    if "all" in chamber_input.lower() or "both" in chamber_input.lower():
        chamber_input_list = [chamber for chamber in chamber_choices]
    elif "," in chamber_input:
        chamber_input_split = chamber_input.replace(" ", "").split(",")
        chamber_input_list = [c.strip() for c in chamber_input_split]
    else:
        chamber_input_list = [chamber_input]
    return chamber_input_list


def process_state_input(state_input: str, state_choices: list):
    if "all but" in state_input.lower():
        state_input_split = state_input[7:].replace(" ", "").split(",")
        excluded_states = [s.strip().upper() for s in state_input_split]
        state_input_list = [s for s in state_choices if s not in excluded_states]
    elif "all starting" in state_input.lower():
        start_state = state_input.split(" ")[-1]
        if start_state in state_choices:
            start_index = state_choices.index(start_state)
            state_input_list = state_choices[start_index:]
    elif "all from" in state_input.lower():
        state_input_split = state_input.split(" ")
        start_state = state_input_split[2]
        end_state = state_input_split[-1]
        if start_state and end_state in state_choices:
            start_index = state_choices.index(start_state)
            end_index = state_choices.index(end_state) + 1
            state_input_list = state_choices[start_index:end_index]
    elif state_input.lower().strip() == "all":
        state_input_list = state_choices
    elif "," in state_input:
        state_input_split = state_input.replace(" ", "").split(",")
        state_input_list = [s.strip().upper() for s in state_input_split]
    else:
        state_input_list = [state_input]
    return state_input_list


def process_district_input(district_input: str, district_choices: list):
    if "all but" in district_input.lower():
        district_input_split = district_input[7:].replace(" ", "").split(",")
        excluded_districts = [d.strip() for d in district_input_split]
        district_input_list = [d for d in district_choices if d not in excluded_districts]
    elif "all starting" in district_input.lower():
        start_district = district_input.split(" ")[-1]
        if start_district in district_choices:
            start_index = district_choices.index(start_index)
            district_input_list = district_choices[start_index:]
    elif "all from" in district_input.lower():
        district_input_split = district_input.split(" ")
        start_district = district_input_split[2]
        end_district = district_input_split[-1]
        if start_district and end_district in district_choices:
            start_index = district_choices.index(start_district)
            end_index = district_choices.index(end_district) + 1
            district_input_list = district_choices[start_index:end_index]
    elif district_input.lower().strip() == "all":
        district_input_list = district_choices
    elif "," in district_input:
        district_input_split = district_input.replace(" ", "").split(",")
        district_input_list = [d.strip().upper() for d in district_input_split]
    else:
        district_input_list = [district_input]
    return district_input_list


def process_candidate_output(candidate_input: str, candidate_choices: list):
    if "all but" in candidate_input.lower():
        candidate_input_split = candidate_input[7:].replace(" ", "").split(",")
        excluded_candidates = [c.strip() for c in candidate_input_split]
        candidate_input_list = [c for c in candidate_choices if c not in excluded_candidates]
    elif "all starting" in candidate_input.lower():
        start_district = candidate_input.split(" ")[-1]
        if start_district in candidate_choices:
            start_index = candidate_choices.index(start_index)
            candidate_input_list = candidate_choices[start_index:]
    elif "all from" in candidate_input.lower():
        candidate_input_split = candidate_input.split(" ")
        start_district = candidate_input_split[2]
        end_district = candidate_input_split[-1]
        if start_district and end_district in candidate_choices:
            start_index = candidate_choices.index(start_district)
            end_index = candidate_choices.index(end_district) + 1
            candidate_input_list = candidate_choices[start_index:end_index]
    elif candidate_input.lower().strip() == "all":
        candidate_input_list = candidate_choices
    elif "," in candidate_input:
        candidate_input_split = candidate_input.replace(" ", "").split(",")
        candidate_input_list = [c.strip().upper() for c in candidate_input_split]
    else:
        candidate_input_list = [candidate_input]
    return candidate_input_list