import sys
import os
from modules.log_creator import create_log_file
from workflows import scrape_all_candidates_in_one_district, scrape_all_districts_in_one_state, scrape_all_states_in_one_chamber
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from user_inputs import get_user_inputs


def main():
    
    create_log_file()

    year, chamber, input_state, input_district, _ = get_user_inputs(chamber = True, action = "scrape")

    if input_state.lower() == "all":
        scrape_all_states_in_one_chamber(year = year, chamber = chamber)
    elif input_district == "all":
        scrape_all_districts_in_one_state(year = year, chamber = chamber, state = input_state)
    elif input_district != "all":
        scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = input_state, district = input_district)


if __name__ == "__main__":
    main()