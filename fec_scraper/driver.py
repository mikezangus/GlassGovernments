import sys
import os
from firefox_driver import firefox_driver
from log_file_creator import create_log_file
from scraper import scrape_all_candidates_in_one_district, scrape_all_districts_in_one_state, scrape_multiple_states


create_log_file()


webdriver = firefox_driver()


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)


sys.path.append(parent_dir)
from user_inputs import get_user_inputs


year, chamber, state, district, _ = get_user_inputs(chamber = True, action = "scrape")
print(year, chamber, state, district, _)


if chamber == "senate":
    scrape_all_candidates_in_one_district(driver = webdriver, year = year, chamber = chamber, state = state)
elif chamber == "house":
    if state.lower() == "all":
        scrape_multiple_states(driver = webdriver, year = year, chamber = chamber)
    if district == "all":
        scrape_all_districts_in_one_state(driver = webdriver, year = year, chamber = chamber, state = state, district = district)
    scrape_all_candidates_in_one_district(driver = webdriver, year = year, chamber = chamber, state = state, district = district)