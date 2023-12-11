import json
import os
from button_clickers import select_results_per_page
from scraper_engine import scrape_one_candidate
from utilities import load_base_url, check_if_district_exists, get_candidate_count


def scrape_all_candidates_in_one_district(driver, year: str, chamber: str, state: str, district: str = None):
    print(f"Starting to scrape all candidates for {state}-{district}")
    if chamber == "house":
        load_base_url(driver = driver, year = year, chamber = chamber, state = state, district = district)
    elif chamber == "senate":
        load_base_url(driver = driver, year = year, chamber = chamber, state = state)
        district = chamber.upper()
    candidate_count = get_candidate_count(driver = driver, state = state, district = district)
    for i in range(1, candidate_count):
        if i >= 9:
            select_results_per_page(driver = driver, year = year, chamber = chamber, state = state, district = district)
        scrape_one_candidate(driver = driver, year = year, chamber = chamber, state = state, district = district, candidate_count = candidate_count, i = i)


def scrape_all_districts_in_one_state(driver, year: str, chamber: str, state: str):
    print(f"Starting to scrape all {state} districts")
    for i in range(1, 100):
        load_base_url(driver = driver, year = year, chamber = chamber, state = state, district = str(i).zfill(2))
        if not check_if_district_exists(driver = driver):
            return
        scrape_all_candidates_in_one_district(driver = driver, year = year, chamber = chamber, state = state, district = str(i).zfill(2))


def scrape_all_states_for_one_chamber(driver, year: str, chamber: str):
    print(f"Starting to scrape all states' {chamber} data for {year}")
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
                scrape_all_candidates_in_one_district(driver = driver, year = year, chamber = chamber, state = state, district = district)
            else:
                scrape_all_districts_in_one_state(driver = driver, year = year, chamber = chamber, state = state)
        elif chamber == "senate":
            scrape_all_candidates_in_one_district