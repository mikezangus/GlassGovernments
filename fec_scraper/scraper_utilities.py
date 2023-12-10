import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from message_generator import generate_message


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
            message = generate_message(action = action, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
            driver.refresh()
    message = generate_message(action = action, attempt = max_attempts, max_attempts = max_attempts)
    print(message)
    logging.info(message)
    return False


def construct_base_url(year: str, chamber: str, state: str, district: str = None):
    if chamber == "house":
        url = f"https://www.fec.gov/data/elections/{chamber}/{state}/{str(district).zfill(2)}/{year}/"
    elif chamber == "senate":
        url = f"https://www.fec.gov/data/elections/{chamber}/{state}/{year}/"
    return url


def load_base_url(driver, year: str, chamber: str, state: str, district: str = None):

    action = "load base url"
    if not district:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state}"
    else:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state} | District: {district}"

    url = construct_base_url(year = year, chamber = chamber, state = state, district = district)

    max_attempts = 25
    for attempt in range(1, max_attempts):
        try:
            driver.get(url)
            load_web_page(driver = driver)
            print(f"Successfully loaded {url}")
            return True
        except Exception as e:
            message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
            time.sleep(10)
    message = generate_message(action = action, subject = subject, attempt = max_attempts, max_attempts = max_attempts)
    print(message)
    logging.info(message)
    return False


def check_if_district_exists(driver):

    action = "check if district exists"

    try:
        locator_financial_totals = (By.CSS_SELECTOR, "#candidate-financial-totals > div:nth-child(2)")
        element_financial_totals = WebDriverWait(driver = driver, timeout = 60).until(
            EC.presence_of_element_located(locator = locator_financial_totals)
        )
        if "we don't have" in element_financial_totals.text.lower():
            return False
        else:
            return True
    except Exception as e:
        message = generate_message(action = action, exception = e)
        print(message)
        logging.info(message)
        logging.info(driver.page_source)
        return False
    

def select_results_per_page(driver, year, chamber, state, district):

    action = "select results per page"
    if not district:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state}"
    else:
        subject = f"Year: {year} | Chamber: {chamber.capitalize()} | State: {state} | District: {district}"

    max_attempts = 25
    for attempt in range(1, max_attempts):
        try:
            locator_results_per_page = (By.CSS_SELECTOR, "#DataTables_Table_0_length > label:nth-child(1) > select:nth-child(1)")
            element_results_per_page = WebDriverWait(driver = driver, timeout = 60).until(
                EC.element_to_be_clickable(locator = locator_results_per_page)
            )
            time.sleep(1)
            Select(webelement = element_results_per_page).select_by_value(value = "100")
            return True
        except Exception as e:
            message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
        driver.refresh()
        time.sleep(10)
    message = generate_message(action = action, subject = subject, attempt = max_attempts, max_attempts = max_attempts)
    print(message)
    logging.info(message)
    return False