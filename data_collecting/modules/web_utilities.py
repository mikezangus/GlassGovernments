import logging
import time
from datetime import datetime, timedelta
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
    max_attempts = 5
    for attempt in range(max_attempts):
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
            driver.refresh()
            if attempt > 1:
                print(message)
    message = write_failure_message(action = action, attempt = attempt, max_attempts = max_attempts)
    logging.info(message)
    return False


def load_base_url(driver, year: str, chamber: str, state: str, district: str = None):
    action = "load base url"
    if district:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state} | District: {district}"
    else:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state}"
    url = construct_base_url(year = year, chamber = chamber, state = state, district = district)
    try:
        driver.get(url)
        load_web_page(driver = driver)
        print(f"Successfully loaded {url}")
        return True
    except Exception as e:
        message = write_failure_message(action = action, subject = subject, exception = e)
        print(message)
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
    

def handle_rate_limit(driver, element):
    wait_time_minutes = 30
    text_downloads_pane = element.text
    if "maximum downloads" in text_downloads_pane.lower() or "server error" in text_downloads_pane.lower():
        current_time = datetime.now()
        end_time = current_time + timedelta(minutes = wait_time_minutes)
        print(f"Rate limit hit at {current_time.strftime('%H:%M:%S')}, trying again in {wait_time_minutes} minutes at {end_time.strftime('%H:%M:%S')}")
        time.sleep(wait_time_minutes * 60)
        print("Wait time over, refreshing page")
        driver.refresh()
        return
    

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