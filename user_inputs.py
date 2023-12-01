import os


def get_user_input(callback, data_dir):

    def is_valid_input(choice, options):
        return choice in options or choice.lower() == "all"

    # 1. Year
    def decide_year():
        years = sorted([y for y in os.listdir(data_dir) if not y.startswith(".")])
        while True:
            year_input = input(str(f"From which year do you want to clean data?:\n{', '.join(years)}\n> "))
            if year_input in years:
                decide_state(year = year_input)
                break
            else:
                print("You've entered an invalid year, try again")

    # 2. State
    def decide_state(year):
        states_dir = os.path.join(data_dir, year)
        states = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
        while True:
            state_input = input(f"From which state do you want to clean files? For all states, enter 'all':\n{', '.join(states)}\n> ").upper()
            if is_valid_input(choice = state_input, options = states):
                if state_input.lower() == "all":
                    process_all_states(year = year)
                else:
                    decide_district(year = year, state = state_input)
                break
            else:
                print("You've entered an invalid state, try again")

    def process_all_states(year):
        print(f"\nCleaning data from {year} for all states\n{'-' * 100}")
        states_dir = os.path.join(data_dir, year)
        states = sorted([s for s in os.listdir(states_dir) if not s.startswith(".")])
        for state in states:
            process_all_districts(year = year, state = state)

    # 3. District
    def decide_district(year, state):
        districts_dir = os.path.join(data_dir, year, state)
        districts = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        if len(districts) == 1:
            decide_candidate(year = year, state = state, district = districts[0])   
        else:
            while True:
                district_input = input(f"From which district do you want to clean files? For all districts, enter 'all':\n{', '.join(districts)}\n> ")
                if is_valid_input(choice = district_input, options = districts):
                    if district_input.lower() == "all":
                        process_all_districts(year = year, state = state)
                    else:
                        decide_candidate(year = year, state = state, district = district_input)
                    break
                else:
                    print("You've entered an invalid district, try again")

    def process_all_districts(year, state):
        print(f"\nCleaning data for all {state} districts\n{'-' * 100}")
        districts_dir = os.path.join(data_dir, year, state)
        districts = sorted([d for d in os.listdir(districts_dir) if not d.startswith(".")])
        for district in districts:
            process_all_candidates(year = year, state = state, district = district)

    # 4. Candidate
    def decide_candidate(year, state, district):
        candidates_dir = os.path.join(data_dir, year, state, district)
        src_file_names = sorted([f for f in os.listdir(candidates_dir) if not f.startswith(".") and f.count("_") == 6])
        candidate_last_names = [file.split("_")[3] for file in src_file_names]
        while True:
            candidate_input = input(f"Which candidate's file do you want to clean? For all candidates, enter 'all':\n{', '.join(candidate_last_names)}\n> ").upper()
            if is_valid_input(choice = candidate_input, options = candidate_last_names):
                if candidate_input.lower() == "all":
                    process_all_candidates(year = year, state = state, district = district)
                else:
                    for src_file_name in src_file_names:
                        if src_file_name.split("_")[3].upper() == candidate_input:
                            process_one_candidate(year = year, state = state, district = district, src_file_name = src_file_name)  
                break
            else:
                print("You've entered an invalid candidate, try again")     
    
    def process_all_candidates(year, state, district):
        print(f"\nCleaning data for all {state}-{district} candidates\n{'-' * 75}")
        candidates_dir = os.path.join(data_dir, year, state, district)
        src_file_names = [f for f in os.listdir(candidates_dir) if not f.startswith(".") and f.count("_") == 6]
        for src_file_name in src_file_names:
            process_one_candidate(year = year, state = state, district = district, src_file_name = src_file_name)
    
    def process_one_candidate(year, state, district, src_file_name):
        callback(year = year, state = state, district = district, src_file_name = src_file_name)

    # 5. Run
    decide_year()
