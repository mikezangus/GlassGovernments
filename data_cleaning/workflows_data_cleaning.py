from engine_data_cleaning import clean_one_candidate


def clean_multiple_candidates(candidate_list: list, year: str, chamber: str, state: str, district: str, raw_data_dir, cleaned_data_dir):
    for raw_file_name in candidate_list:
        clean_one_candidate(raw_file_name, year, chamber, state, district, raw_data_dir, cleaned_data_dir)


def clean_multiple_districts(district_list: list, candidate_list: list, year: str, chamber: str, state: str, district: str, raw_data_dir, cleaned_data_dir):
    for district in district_list:
        clean_multiple_candidates(candidate_list, year, chamber, state, district, raw_data_dir, cleaned_data_dir)


def clean_multiple_states(state_list: list, chamber: str, district_list: list, candidate_list: list, year: str, district: str, raw_data_dir, cleaned_data_dir):
    for state in state_list:
        if "house" in chamber:
            clean_multiple_districts(district_list, candidate_list, year, chamber, state, district, raw_data_dir, cleaned_data_dir)
        elif "senate" in chamber:
            clean_multiple_candidates(candidate_list, year, chamber, state, district, raw_data_dir, cleaned_data_dir)


def determine_workflow(year: str, chamber_list: list, state_list: list, district_list: list, candidate_list: list, raw_data_dir, cleaned_data_dir):
    
    # 1. Chamber
    if len(chamber_list) > 1:
        for chamber in chamber_list:
            clean_multiple_states(state_list, chamber, district_list, raw_file_name, year, district_list, raw_data_dir, cleaned_data_dir)
    else:
        chamber = chamber_list[0].lower()
    
    # 2. State
    if len(state_list) > 1:
        clean_multiple_states(state_list, chamber, district_list, raw_file_name, year, district_list, raw_data_dir, cleaned_data_dir)
    else:
        state = state_list[0]

    # 3. District
    if len(district_list) > 1:
        for district in district_list:
            clean_multiple_candidates(candidate_list, year, chamber, state, district, raw_data_dir, cleaned_data_dir)
    else:
        district = district_list[0]

    # 4. Candidate
    if len(candidate_list) > 1:
        clean_multiple_candidates(candidate_list, year, chamber, state, district, raw_data_dir, cleaned_data_dir)
    else:
        raw_file_name = candidate_list[0]
        clean_one_candidate(raw_file_name, year, chamber, state, district, raw_data_dir, cleaned_data_dir)