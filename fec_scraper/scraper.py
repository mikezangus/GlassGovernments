import json
import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from scraper_one_candidate import scrape_one_candidate
from scraper_utilities import load_base_url, check_if_district_exists, select_results_per_page

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
# sys.path.append(parent_dir)
with open(os.path.join(parent_dir, "us_states_all.json"), "r") as us_states_all_file:
    us_states_all = json.load(us_states_all_file)
with open(os.path.join(parent_dir, "us_states_at_large.json"), "r") as us_states_at_large_file:
    us_states_at_large = json.load(us_states_at_large_file)


def scrape_all_candidates_in_one_district(driver, year: str, chamber: str, state: str, district: str = None):
    print(f"Starting to scrape all {state}-{district} candidates")
    load_base_url(driver = driver, year = year, chamber = chamber, state = state, district = district)
    if not check_if_district_exists(driver = driver):
        return
    try:
        locator_candidate_count = (By.CSS_SELECTOR, "#DataTables_Table_0_info")
        element_candidate_count = WebDriverWait(driver = driver, timeout = 60).until(
            lambda d: d.find_element(*locator_candidate_count) if EC.text_to_be_present_in_element(
                locator = locator_candidate_count,
                text_ = "Showing"
            )(d) else False
        )
        candidate_count = int(element_candidate_count.text.split(" ")[-2])
    except Exception as e:
        return
    for i in range(candidate_count):
        load_base_url(driver = driver, year = year, chamber = chamber, state = state, district = district)
        if i >= 9:
            while not select_results_per_page(driver = driver):
                select_results_per_page(driver = driver)
        scrape_one_candidate(driver = driver, chamber = chamber, year = year, state = state, district = district, candidate_count = candidate_count, i = i)
    return


def scrape_all_districts_in_one_state(driver, year, chamber, state):
    if state in us_states_at_large.values():
        district = "00"
        scrape_all_candidates_in_one_district(driver = driver, year = year, chamber = chamber, state = state, district = district)
    print(f"Starting to scrape all {state} districts")
    for district in range(1, 100):
        load_base_url(driver = driver, year = year, chamber = chamber, state = state, district = district)
        if not check_if_district_exists(driver = driver):
            return
        else:
            scrape_all_candidates_in_one_district(driver = driver, year = year, chamber = chamber, state = state, district = district)


def scrape_multiple_states(driver, year, chamber):
    for state in us_states_all.values():
        scrape_all_districts_in_one_state(driver = driver, year = year, chamber = chamber, state = state)