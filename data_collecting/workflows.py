import logging
import os
import sys

from engine import scrape_one_candidate
from modules.sub_modules.element_locators import locator_candidate_count, locator_financial_totals
from modules.sub_modules.firefox_driver import firefox_driver
from modules.sub_modules.message_writer import write_failure_message
from modules.sub_modules.web_utilities import load_base_url, verify_district_exists, get_candidate_count

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from us_states.us_state_loader import load_states


def scrape_all_candidates_in_one_district(year: str, chamber: str, state: str, district: str = None):  


    def quit_driver(driver):
        print("Quitting driver")
        driver.quit()   


    def load_district(driver, subject, year: str, state: str, district: str = None):
        load_base_url(driver, subject, year, state, district)
        if not verify_district_exists(driver, subject, locator_financial_totals):
            return False, None, None
        candidate_count = get_candidate_count(driver, subject, locator_candidate_count)
        if candidate_count is None:
            return False, None, None
        return True, candidate_count


    def scrape_district(candidate_count: int, chamber: str, district: str = None):
        if district:
            subject_district = district
        else:
            subject_district = chamber.upper()
        print(f"\n{'-' * 100}\n{'-' * 100}\nStarting to scrape all {candidate_count} candidates for {state}-{subject_district}")
        for candidate in range(1, candidate_count + 1):
            action = "scrape"
            subject = f"{state}-{subject_district} candidate {candidate}/{candidate_count}"
            try:
                if not scrape_one_candidate(driver, subject, year, chamber, state, candidate, district):
                    message = f"Skipping {subject}"
                    print(message)
                    continue
            except Exception as e:
                message = f"{write_failure_message(action, subject, None, None, e)}\n{'-' * 100}"
                print(message)
                logging.error(message)
                continue


    print("Starting Firefox driver")
    driver = firefox_driver()
    if not district:
        subject = f"Year: {year} | Chamber: {chamber} | State: {state}"
    else:
        subject = f"Year: {year} | Chamber: {chamber} | State: {state} | District: {district}"
    district_loaded, candidate_count = load_district(driver, subject, year, state, district)
    if district_loaded:
        scrape_district(candidate_count, chamber, district)
        quit_driver(driver)
        return True
    quit_driver(driver)
    return False


def scrape_multiple_districts(year: str, chamber: str, state: str, district_list: list):
    print(f"Dist list: {district_list}")
    for district in district_list:
        print(f"Dist: {district}")
        if not scrape_all_candidates_in_one_district(year, chamber, state, district):
            break


def scrape_multiple_states(year: str, chamber: str, state_list: list, us_states_at_large_list: list, district_list: list):
    for state in state_list:
        if chamber.lower() == "house":
            if state in us_states_at_large_list:
                scrape_all_candidates_in_one_district(year, chamber, state, "00")
            else:
                scrape_multiple_districts(year, chamber, state, district_list)
        elif chamber.lower() == "senate":
            scrape_all_candidates_in_one_district(year, chamber, state)
        

def scrape_multiple_chambers(year: str, chamber_list: list, state_list: list, us_states_at_large_list: list, district_list: list):
    for chamber in chamber_list:
        scrape_multiple_states(year, chamber, state_list, us_states_at_large_list, district_list)


def determine_workflow(year: str, chamber_list: list, state_list: list, district_list: list):

    print(f"Dist list via determine workflow: {district_list}")

    _, us_states_at_large_list = load_states()

    if len(chamber_list) > 1:
        scrape_multiple_chambers(year, chamber_list, state_list, us_states_at_large_list, district_list)
    else:
        chamber = chamber_list[0].lower()

    if len(state_list) > 1:
        scrape_multiple_states(year, chamber, state_list, us_states_at_large_list, district_list)
    else:
        state = state_list[0]

    if len(district_list) > 1:
        scrape_multiple_districts(year, chamber, state, district_list)
    else:
        district = district_list[0]
        scrape_all_candidates_in_one_district(year, chamber, state, district)