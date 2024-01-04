import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from engine import scrape_one_candidate
from modules.sub_modules.element_locators import locator_financial_totals, locator_candidate_count
from modules.sub_modules.firefox_driver import firefox_driver
from modules.sub_modules.message_writer import write_failure_message
from modules.sub_modules.web_utilities import load_base_url


def verify_constituency_exists(driver, subject):
    action = f"verify existence"
    try:
        element_financial_totals = WebDriverWait(driver, 60).until(EC.presence_of_element_located(locator_financial_totals))
        if "we don't have" in element_financial_totals.text.lower():
            print(f"{subject} doesn't exist")
            return False
        return True
    except Exception as e:
        message = write_failure_message(action, subject, exception = e)
        print(message)
        logging.info(message)
        logging.info(driver.page_source)
        return False


def get_candidate_count(driver, subject):
    action = "get candidate count"
    try:
        WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element(locator_candidate_count, "Showing"))
        element_candidate_count = driver.find_element(*locator_candidate_count)
        candidate_count = int(element_candidate_count.text.split(" ")[-2])
        return candidate_count
    except Exception as e:
        message = write_failure_message(action, subject, exception = e)
        print(message)
        logging.info(message)
        return None


def scrape_candidates(driver, action: str, year: str, chamber: str, state: str, candidate_count: int, district: str = None):
    if district:
        subject_district = district
    else:
        subject_district = chamber.upper()
    print(f"\n{'-' * 100}\n{'-' * 100}\nStarting to scrape all {candidate_count} candidates for {state}-{subject_district}")
    for candidate in range(1, candidate_count + 1):
        subject = f"{state}-{subject_district} candidate {candidate}/{candidate_count}"
        if not scrape_one_candidate(driver, action, subject, year, chamber, state, candidate, district):
            message = f"Skipping {subject}"
            print(message)
    return


def scrape_constituency(action: str, year: str, chamber: str, state: str, district: str = None):
    driver_loaded, driver = firefox_driver()
    if not driver_loaded:
        return False, "driver_not_loaded"
    print("Starting Firefox driver")
    if district:
        subject = f"Year: {year} | Chamber: {chamber} | State: {state} | District: {district}"
    else:
        subject = f"Year: {year} | Chamber: {chamber} | State: {state}"
    load_base_url(driver, subject, year, chamber, state, district)
    if not verify_constituency_exists(driver, subject):
        return False, None
    candidate_count = get_candidate_count(driver, subject)
    if candidate_count is None:
        return False, None
    scrape_candidates(driver, action, year, chamber, state, candidate_count, district)
    print("Quitting Firefox driver\n")
    driver.quit() 
    return True, None