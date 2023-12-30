from engine import clean_one_candidate


def clean_multiple_candidates(year: str, chamber: str, state: str, candidate_list: list, raw_data_dir: str, cleaned_data_dir: str, district: str = None):
    for candidate in candidate_list:
        clean_one_candidate(year, chamber, state, candidate, raw_data_dir, cleaned_data_dir, district)


def clean_multiple_districts(year: str, chamber: str, state: str, district_list: list, candidate_list: list, raw_data_dir: str, cleaned_data_dir: str):
    for district in district_list:
        clean_multiple_candidates(year, chamber, state, candidate_list, raw_data_dir, cleaned_data_dir, district)


def clean_multiple_states(year: str, chamber: str, state_list: list, district_list: list, candidate_list: list, raw_data_dir: str, cleaned_data_dir: str):
    for state in state_list:
        if chamber.lower() == "house":
            clean_multiple_districts(year, chamber, state, district_list, candidate_list, raw_data_dir, cleaned_data_dir)
        elif chamber.lower() == "senate":
            clean_multiple_candidates(year, chamber, state, candidate_list, raw_data_dir, cleaned_data_dir)


def clean_multiple_chambers(year: str, chamber_list: list, state_list: list, district_list: list, candidate_list: list, raw_data_dir: str, cleaned_data_dir: str):
    for chamber in chamber_list:
        clean_multiple_states(year, chamber, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)


def clean_multiple_years(year_list: list, chamber_list: list, state_list: list, district_list: list, candidate_list: list, raw_data_dir: str, cleaned_data_dir: str):
    for year in year_list:
        clean_multiple_chambers(year, chamber_list, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)


def determine_workflow(year_list: list, chamber_list: list, state_list: list, district_list: list, candidate_list: list, raw_data_dir: str, cleaned_data_dir: str):

    if len(year_list) > 1:
        clean_multiple_years(year_list, chamber_list, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)
    else:
        year = year_list[0]
    
    if len(chamber_list) > 1:
        clean_multiple_chambers(year, chamber_list, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)
    else:
        chamber = chamber_list[0].lower()
    
    if len(state_list) > 1:
        clean_multiple_states(year, chamber, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)
    else:
        state = state_list[0].upper()

    if len(district_list) > 1:
        clean_multiple_districts(year, state, district_list, candidate_list, raw_data_dir, cleaned_data_dir)
    else:
        district = district_list[0].upper()

    if len(candidate_list) > 1:
        clean_multiple_candidates(year, chamber, state, candidate_list, raw_data_dir, cleaned_data_dir, district)
    else:
        candidate = candidate_list[0]
        clean_one_candidate(year, chamber, state, candidate, raw_data_dir, cleaned_data_dir, district)