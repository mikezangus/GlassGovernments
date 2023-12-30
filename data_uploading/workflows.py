from engine import upload_one_candidate


def upload_multiple_candidates(year: str, chamber: str, state: str, candidate_list: list, district: str = None):
    for candidate in candidate_list:
        upload_one_candidate(year, chamber, state, district, candidate)


def upload_multiple_districts(year: str, chamber: str, state: str, district_list: list, candidate_list: list):
    for district in district_list:
        upload_multiple_candidates(year, chamber, state, district, candidate_list)


def upload_multiple_states(year: str, chamber: str, state_list: list, district_list: list, candidate_list: list):
    for state in state_list:
        if chamber.lower() == "house":
            upload_multiple_districts(year, chamber, state, district_list, candidate_list)
        elif chamber.lower() == "senate":
            upload_multiple_candidates(year, chamber, state, candidate_list)


def upload_multiple_chambers(year: str, chamber_list: list, state_list: list, district_list: list, candidate_list: list):
    for chamber in chamber_list:
        upload_multiple_states(year, chamber, state_list, district_list, candidate_list)


def determine_workflow(year: str, chamber_list: list, state_list: list, district_list: list, candidate_list: list):

    if len(chamber_list) > 1:
        upload_multiple_chambers(year, chamber_list, state_list, district_list, candidate_list)
    else:
        chamber = chamber_list[0].lower()

    if len(state_list) > 1:
        upload_multiple_states(year, chamber, state_list, district_list, candidate_list)
    else:
        state = state_list[0].upper()

    if len(district_list) > 1:
        upload_multiple_districts(year, chamber, state, district_list, candidate_list)
    else:
        district = district_list[0].upper()

    if len(candidate_list) > 1:
        upload_multiple_candidates(year, chamber, state, district, candidate_list)
    else:
        candidate = candidate_list[0]
        upload_one_candidate(year, chamber, state, district, candidate)