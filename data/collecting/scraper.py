import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from engine import scrape_one_candidate
from firefox.firefox_driver import firefox_driver
from modules.sub_modules.element_locators import locator_financial_totals, locator_candidate_count
from modules.sub_modules.message_writer import write_failure_message
from modules.sub_modules.web_utilities import load_base_url


def verify_constituency_exists(driver, subject):
    action = f"verify existence"
    try:
        element_financial_totals = WebDriverWait(driver, 60).until(EC.presence_of_element_located(locator_financial_totals))
        if "we don't have" in element_financial_totals.text.lower():
            print(f"{subject} | Doesn't exist")
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


def scrape_candidates(driver, action, subject, year: str, chamber: str, state: str, candidate_count: int, district: str = None):
    print(f"\n{'-' * 100}\n{'-' * 100}\n{subject} | Starting to {action} all {candidate_count} candidates")
    for candidate in range(1, candidate_count + 1):
        subject = None
        if chamber.lower() == "house":
            subject = f"{year} {state}-{district} [{candidate}/{candidate_count}]"
        elif chamber.lower() == "senate":
            subject = f"{year} {state}-{chamber} [{candidate}/{candidate_count}]"
        if not scrape_one_candidate(driver, action, subject, year, chamber, state, candidate, district):
            message = f"{subject} | Skipping"
            print(message)
    return


def scrape_constituency(action: str, year: str, chamber: str, state: str, district: str = None):
    try:
        _, driver = firefox_driver()
        if not driver:
            print(f"\nFailed to load Firefox driver\n")
            return False
        print("\nStarting Firefox driver\n")
        subject = None
        if chamber.lower() == "house":
            subject = f"{year} {state}-{district}"
        elif chamber.lower() == "senate":
            subject = f"{year} {state}-{chamber}"
        load_base_url(driver, subject, year, chamber, state, district)
        if not verify_constituency_exists(driver, subject):
            return False
        candidate_count = get_candidate_count(driver, subject)
        if candidate_count is None:
            return False
        scrape_candidates(driver, action, subject, year, chamber, state, candidate_count, district)
        print("\nQuitting Firefox driver\n")
        driver.quit()
        return True
    except Exception as e:
        print(f"Exception occured in the scrape_constituency function:\n{e}")