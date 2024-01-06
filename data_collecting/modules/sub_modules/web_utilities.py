import logging
import time
from datetime import datetime, timedelta
from selenium.webdriver.support.ui import WebDriverWait
from .message_writer import write_failure_message


def construct_base_url(year: str, chamber: str, state: str, district: str = None):
    if chamber.lower() == "house":
        url = f"https://www.fec.gov/data/elections/house/{state}/{district}/{year}/"
    elif chamber.lower() == "senate":
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


def load_base_url(driver, subject, year: str, chamber: str, state: str, district: str = None):
    action = "load base url"
    url = construct_base_url(year, chamber, state, district)
    try:
        driver.get(url)
        load_web_page(driver, subject)
        print(f"{subject} | Successfully loaded {url}")
        return True
    except Exception as e:
        message = write_failure_message(action, subject, exception = e)
        print(message)
        logging.info(message)
        return False
    

def handle_rate_limit(driver, subject, element):
    wait_time_minutes = 30
    text_downloads_pane = element.text
    if "maximum downloads" in text_downloads_pane.lower() or "server error" in text_downloads_pane.lower():
        current_time = datetime.now()
        end_time = current_time + timedelta(minutes = wait_time_minutes)
        print(f"{subject} | Rate limit hit at {current_time.strftime('%H:%M:%S')}, trying again in {wait_time_minutes} minutes at {end_time.strftime('%H:%M:%S')}")
        time.sleep(wait_time_minutes * 60)
        resume_time = datetime.now()
        print(f"{subject} | Rate limit wait over at {resume_time.strftime('%H:%M:%S')}, refreshing page and trying again")
        driver.refresh()
        return