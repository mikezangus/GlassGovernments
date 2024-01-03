def process_year_input_str(year_input_str: str, year_choices_list: list):
    if "all" in year_input_str.lower():
        year_input_list = year_choices_list
    elif "," in year_input_str:
        year_input_split = year_input_str.replace(" ", "").split(",")
        year_input_list = [y.strip() for y in year_input_split]
    else:
        year_input_list = [year_input_str]
    return year_input_list


def process_chamber_input_str(chamber_input_str: str, chamber_choices_list: list):
    if "all" in chamber_input_str.lower() or "both" in chamber_input_str.lower():
        chamber_input_list = [chamber for chamber in chamber_choices_list]
    elif "," in chamber_input_str:
        chamber_input_split = chamber_input_str.replace(" ", "").split(",")
        chamber_input_list = [c.strip() for c in chamber_input_split]
    else:
        chamber_input_list = [chamber_input_str]
    return chamber_input_list


def process_state_input_str(state_input_str: str, state_choices_list: list):
    if "all but" in state_input_str.lower():
        state_input_split = state_input_str[7:].replace(" ", "").split(",")
        excluded_states = [s.strip().upper() for s in state_input_split]
        state_input_list = [s for s in state_choices_list if s not in excluded_states]
    elif "all starting" in state_input_str.lower():
        start_state = state_input_str.split(" ")[-1]
        if start_state in state_choices_list:
            start_index = state_choices_list.index(start_state)
            state_input_list = state_choices_list[start_index:]
    elif "all from" in state_input_str.lower():
        state_input_split = state_input_str.split(" ")
        start_state = state_input_split[2]
        end_state = state_input_split[-1]
        if start_state and end_state in state_choices_list:
            start_index = state_choices_list.index(start_state)
            end_index = state_choices_list.index(end_state) + 1
            state_input_list = state_choices_list[start_index:end_index]
    elif state_input_str.lower().strip() == "all":
        state_input_list = state_choices_list
    elif "," in state_input_str:
        state_input_split = state_input_str.replace(" ", "").split(",")
        state_input_list = [s.strip().upper() for s in state_input_split]
    else:
        state_input_list = [state_input_str]
    return state_input_list


def process_district_input_str(district_input_str: str, district_choices_list: list):
    if "all but" in district_input_str.lower():
        district_input_split = district_input_str[7:].replace(" ", "").split(",")
        excluded_districts = [d.strip() for d in district_input_split]
        district_input_list = [d for d in district_choices_list if d not in excluded_districts]
    elif "all starting" in district_input_str.lower():
        start_district = district_input_str.split(" ")[-1]
        if start_district in district_choices_list:
            start_index = district_choices_list.index(start_index)
            district_input_list = district_choices_list[start_index:]
    elif "all from" in district_input_str.lower():
        district_input_split = district_input_str.split(" ")
        start_district = district_input_split[2]
        end_district = district_input_split[-1]
        if start_district and end_district in district_choices_list:
            start_index = district_choices_list.index(start_district)
            end_index = district_choices_list.index(end_district) + 1
            district_input_list = district_choices_list[start_index:end_index]
    elif district_input_str.lower().strip() == "all":
        district_input_list = district_choices_list
    elif "," in district_input_str:
        district_input_split = district_input_str.replace(" ", "").split(",")
        district_input_list = [d.strip().upper() for d in district_input_split]
    else:
        district_input_list = [district_input_str]
    return district_input_list


def process_candidate_output_str(candidate_input_str: str, candidate_choices_list: list):
    if "all but" in candidate_input_str.lower():
        candidate_input_split = candidate_input_str[7:].replace(" ", "").split(",")
        excluded_candidates = [c.strip() for c in candidate_input_split]
        candidate_input_list = [c for c in candidate_choices_list if c not in excluded_candidates]
    elif "all starting" in candidate_input_str.lower():
        start_district = candidate_input_str.split(" ")[-1]
        if start_district in candidate_choices_list:
            start_index = candidate_choices_list.index(start_index)
            candidate_input_list = candidate_choices_list[start_index:]
    elif "all from" in candidate_input_str.lower():
        candidate_input_split = candidate_input_str.split(" ")
        start_district = candidate_input_split[2]
        end_district = candidate_input_split[-1]
        if start_district and end_district in candidate_choices_list:
            start_index = candidate_choices_list.index(start_district)
            end_index = candidate_choices_list.index(end_district) + 1
            candidate_input_list = candidate_choices_list[start_index:end_index]
    elif candidate_input_str.lower().strip() == "all":
        candidate_input_list = candidate_choices_list
    elif "," in candidate_input_str:
        candidate_input_split = candidate_input_str.replace(" ", "").split(",")
        candidate_input_list = [c.strip().upper() for c in candidate_input_split]
    else:
        candidate_input_list = [candidate_input_str]
    return candidate_input_list