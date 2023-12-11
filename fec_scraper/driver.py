import sys
import os
from modules.firefox_driver import firefox_driver
from modules.log_creator import create_log_file
from workflows import scrape_all_candidates_in_one_district, scrape_all_districts_in_one_state, scrape_all_states_for_one_chamber
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from user_inputs import get_user_inputs


def main():
    
    create_log_file()
    webdriver = firefox_driver()

    year, chamber, state, district, _ = get_user_inputs(chamber = True, action = "scrape")

    if isinstance(state, str) and state.lower() == "all":
        scrape_all_states_for_one_chamber(driver = webdriver, year = year, chamber = chamber)
    elif district == "all":
        scrape_all_districts_in_one_state(driver = webdriver, year = year, chamber = chamber, state = state)
    else:
        scrape_all_candidates_in_one_district(driver = webdriver, year = year, chamber = chamber, state = state, district = district)


if __name__ == "__main__":
    main()