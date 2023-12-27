import json
import logging
import os
from engine import scrape_one_candidate
from modules.button_clickers import select_results_per_page
from modules.element_locators import locator_candidate_count, locator_financial_totals
from modules.firefox_driver import firefox_driver
from modules.utilities import load_base_url, verify_district_exists, get_candidate_count


def scrape_all_candidates_in_one_district(year: str, chamber: str, state: str, district: str = None):

    webdriver = firefox_driver()

    if chamber.lower() == "house":
        district = str(district).zfill(2)
        load_base_url(driver = webdriver, year = year, chamber = chamber, state = state, district = district)
    elif chamber.lower() == "senate":
        district = chamber.upper()
        load_base_url(driver = webdriver, year = year, chamber = chamber, state = state)

    if not verify_district_exists(driver = webdriver, state = state, district = district, locator = locator_financial_totals):
        return False

    candidate_count = get_candidate_count(driver = webdriver, locator = locator_candidate_count, state = state, district = district)
    if candidate_count is None:
        return True
    
    
    print(f"\nStarting to scrape all {candidate_count} candidates for {state}-{district}")
    for candidate in range(1, candidate_count):

        if candidate > 1:
            webdriver = firefox_driver()

        if chamber.lower() == "house":
            load_base_url(driver = webdriver, year = year, chamber = chamber, state = state, district = district)
        elif chamber.lower() == "senate":
            load_base_url(driver = webdriver, year = year, chamber = chamber, state = state)

        if candidate >= 10:
            select_results_per_page(driver = webdriver, chamber = chamber, state = state, district = district)

        if not scrape_one_candidate(driver = webdriver, year = year, chamber = chamber, state = state, district = district, candidate_count = candidate_count, candidate = candidate):
            message = f"Skipping {state}-{district} candidate {candidate}/{candidate_count}"
            print(message)
            logging.info(message)

        webdriver.quit()

    return True


def scrape_all_districts_in_one_state(year: str, chamber: str, state: str):
    print(f"\nStarting to scrape all {state} districts")
    for loop_district in range(1, 100):
        if not scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state, district = loop_district):
            break


def scrape_all_states_in_one_chamber(year: str, chamber: str):
    print(f"\nStarting to scrape all states' {chamber.capitalize()} data in {year}")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    with open(os.path.join(parent_dir, "us_states_all.json"), "r") as us_states_all_file:
        us_states_all = json.load(us_states_all_file)
    with open(os.path.join(parent_dir, "us_states_at_large.json"), "r") as us_states_at_large_file:
        us_states_at_large = json.load(us_states_at_large_file)

    for state in us_states_all.values():
        if chamber == "house":
            if state in us_states_at_large.values():
                district = "00"
                scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state, district = district)
            else:
                scrape_all_districts_in_one_state(year = year, chamber = chamber, state = state)
            
        elif chamber == "senate":
            scrape_all_candidates_in_one_district(year = year, chamber = chamber, state = state)
        else:
            return