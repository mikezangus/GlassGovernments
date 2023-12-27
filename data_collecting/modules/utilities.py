import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .message_writer import write_failure_message


def construct_base_url(year: str, chamber: str, state: str, district: str = None):
    if chamber.lower() == "house":
        url = f"https://www.fec.gov/data/elections/house/{state}/{district}/{year}/"
    elif chamber.lower() == "senate":
        url = f"https://www.fec.gov/data/elections/senate/{state}/{year}/"
    return url


def load_web_page(driver):
    action = "load page"
    timeout_seconds = 60
    max_attempts = 10
    for attempt in range(1, max_attempts):
        try:
            WebDriverWait(driver = driver, timeout = timeout_seconds).until(
                lambda d: d.execute_script("return jQuery.active==0")
            )
            WebDriverWait(driver = driver, timeout = timeout_seconds).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:  
            message = write_failure_message(action = action, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
            driver.refresh()
    return False


def load_base_url(driver, year: str, chamber: str, state: str, district: str = None):

    action = "load base url"
    if district:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state} | District: {district}"
    else:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state}"

    url = construct_base_url(year = year, chamber = chamber, state = state, district = district)

    max_attempts = 25
    for attempt in range(1, max_attempts):
        try:
            driver.get(url)
            load_web_page(driver = driver)
            print(f"Successfully loaded {url}")
            return True
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
            time.sleep(10)

    logging.info(message)
    return False


def verify_district_exists(driver, state: str, district: str, locator: tuple):
    action = f"verify existence"
    subject = f"{state}-{district}"
    try:
        element_financial_totals = WebDriverWait(driver = driver, timeout = 60).until(
            EC.presence_of_element_located(locator = locator)
        )
        if "we don't have" in element_financial_totals.text.lower():
            print(f"{subject} doesn't exist")
            return False
        else:
            return True
    except Exception as e:
        message = write_failure_message(action = action, subject = subject, exception = e)
        print(message)
        logging.info(message)
        logging.info(driver.page_source)
        return False
    

def handle_rate_limit(driver, locator: tuple, state: str, district: str, first_name: str, last_name: str):
    action = "handle rate limit"
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    wait_time_minutes = 30
    try:
        element_downloads_pane = WebDriverWait(driver = driver, timeout = 30).until(
            EC.presence_of_element_located(locator = locator)
        )
        text_downloads_pane = element_downloads_pane.text.lower()
        if "exceeded your maximum downloads" in text_downloads_pane.lower():
            print(f"Rate limit hit, trying again in 30 minutes")
            time.sleep(wait_time_minutes * 60)
        else:
            print(f"Rate limit appears to be gone, continuing now")
            return True
    except Exception as e:
        message = write_failure_message(action = action, subject = subject, exception = e)
        print(message)
        logging.info(message)
        return False
    

def get_candidate_count(driver, locator: tuple, state: str, district: str = None):
    action = "get candidate count"
    subject = f"{state}-{district}"
    try:
        WebDriverWait(driver = driver, timeout = 60).until(
            EC.text_to_be_present_in_element(locator = locator, text_ = "Showing")
        )
        element_candidate_count = driver.find_element(*locator)
        candidate_count = int(element_candidate_count.text.split(" ")[-2])
        return candidate_count
    except Exception as e:
        message = write_failure_message(action = action, subject = subject, exception = e)
        print(message)
        logging.info(message)
        return None