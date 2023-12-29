import logging
import os
import sys

from engine_data_collection import scrape_one_candidate
from modules.button_clickers import select_results_per_page
from modules.element_locators import locator_candidate_count, locator_financial_totals
from modules.firefox_driver import firefox_driver
from modules.message_writer import write_failure_message
from modules.web_utilities import load_base_url, verify_district_exists, get_candidate_count

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import us_states_dir
sys.path.append(us_states_dir)
from us_state_loader import load_states


def scrape_all_candidates_in_one_district(year: str, chamber: str, state: str, district: str = None):

    webdriver = firefox_driver()

    if chamber.lower() == "house":
        district = str(district).zfill(2)
        load_base_url(driver = webdriver, year = year, chamber = chamber, state = state, district = district)
    elif chamber.lower() == "senate":
        district = chamber.upper()
        load_base_url(driver = webdriver, year = year, chamber = chamber, state = state)

    if not verify_district_exists(driver = webdriver, state = state, district = district, locator = locator_financial_totals):
        webdriver.quit()
        return False

    candidate_count = get_candidate_count(driver = webdriver, locator = locator_candidate_count, state = state, district = district)
    if candidate_count is None:
        webdriver.quit()
        return True
    
    print(f"\n{'-' * 100}\n{'-' * 100}\nStarting to scrape all {candidate_count} candidates for {state}-{district}")
    for candidate in range(1, candidate_count + 1):
        action = "scrape"
        subject = f"{state}-{district} candidate {candidate}/{candidate_count}"
        try:
            if chamber.lower() == "house":
                load_base_url(driver = webdriver, year = year, chamber = chamber, state = state, district = district)
            elif chamber.lower() == "senate":
                load_base_url(driver = webdriver, year = year, chamber = chamber, state = state)
            if candidate > 9:
                select_results_per_page(driver = webdriver, chamber = chamber, state = state, district = district)
            if not scrape_one_candidate(driver = webdriver, year = year, chamber = chamber, state = state, district = district, candidate_count = candidate_count, candidate = candidate):
                message = f"Skipping {state}-{district} candidate {candidate}/{candidate_count}"
                print(message)
        except Exception as e:
            message = f"{write_failure_message(action = action, subject = subject, exception = e)}\n{'-' * 100}"
            print(message)
            logging.error(message)
            continue

    webdriver.quit()
    return True
    

def scrape_all_districts_in_one_state(year: str, chamber: str, state: list, us_states_at_large: list):
    print(f"\n{'-' * 100}\n{'-' * 100}\n{'-' * 100}\nStarting to scrape all {state} districts")
    if state in us_states_at_large:
        district = "00"
        scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state, district = district)
    else:
        for loop_district in range(1, 100):
            if not scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state, district = loop_district):
                break
        

def scrape_both_chambers(year: str, us_states_all: list, us_states_at_large: list):
    chambers = ["house", "senate"]
    for chamber in chambers:
        for state in us_states_all:
            scrape_all_districts_in_one_state(year = year, chamber = chamber, state = state, us_states_at_large = us_states_at_large)


def determine_workflow(year, chamber, state, district):
    us_states_all, us_states_at_large = load_states()
    if len(chamber) > 1:
        scrape_both_chambers(year = year, us_states_all = us_states_all, us_states_at_large = us_states_at_large)
    elif len(state) > 1:
        for s in state:
            if chamber.lower() == "house":
                scrape_all_districts_in_one_state(year = year, chamber = chamber, state = s, us_states_at_large = us_states_at_large)
            elif chamber.lower() == "senate":
                scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = s)
    elif len(state) == 1:
        state = state[0]
        if len(district) > 1:
            for d in district:
                if not scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state, district = d):
                    break
        else:
            district = district[0]
            scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state, district = district)