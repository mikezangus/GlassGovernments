import logging
import time
from datetime import datetime, timedelta
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .message_writer import write_failure_message


def construct_base_url(year: str, state: str, district: str = None):
    if district:
        url = f"https://www.fec.gov/data/elections/house/{state}/{district}/{year}/"
    else:
        url = f"https://www.fec.gov/data/elections/senate/{state}/{year}/"
    return url


def load_web_page(driver, subject):
    action = "load page"
    timeout_seconds = 60
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            WebDriverWait(driver, timeout_seconds).until(lambda d: d.execute_script("return jQuery.active==0"))
            WebDriverWait(driver, timeout_seconds).until(lambda d: d.execute_script("return document.readyState") == "complete")
            return True
        except Exception as e:  
            message = write_failure_message(action, subject, attempt, max_attempts, e)
            driver.refresh()
            if attempt > 1:
                print(message)
    message = write_failure_message(action, subject, attempt, max_attempts)
    logging.info(message)
    return False


def load_base_url(driver, subject, year: str, state: str, district: str = None):
    action = "load base url"
    url = construct_base_url(year, state, district)
    try:
        driver.get(url)
        load_web_page(driver, subject)
        print(f"Successfully loaded {url}")
        return True
    except Exception as e:
        message = write_failure_message(action, subject, exception = e)
        print(message)
        logging.info(message)
        return False


def verify_district_exists(driver, subject, locator: tuple):
    action = f"verify existence"
    try:
        element_financial_totals = WebDriverWait(driver, 60).until(EC.presence_of_element_located(locator = locator))
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
    

def handle_rate_limit(driver, element):
    wait_time_minutes = 30
    text_downloads_pane = element.text
    if "maximum downloads" in text_downloads_pane.lower() or "server error" in text_downloads_pane.lower():
        current_time = datetime.now()
        end_time = current_time + timedelta(minutes = wait_time_minutes)
        print(f"Rate limit hit at {current_time.strftime('%H:%M:%S')}, trying again in {wait_time_minutes} minutes at {end_time.strftime('%H:%M:%S')}")
        time.sleep(wait_time_minutes * 60)
        resume_time = datetime.now()
        print(f"Rate limit wait over at {resume_time.strftime('%H:%M:%S')}, refreshing page and trying again")
        driver.refresh()
        return
    

def get_candidate_count(driver, subject, locator: tuple):
    action = "get candidate count"
    try:
        WebDriverWait(driver, 60).until(EC.text_to_be_present_in_element(locator, "Showing"))
        element_candidate_count = driver.find_element(*locator)
        candidate_count = int(element_candidate_count.text.split(" ")[-2])
        return candidate_count
    except Exception as e:
        message = write_failure_message(action, subject, exception = e)
        print(message)
        logging.info(message)
        return None