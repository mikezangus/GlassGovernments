import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from .download_manager import find_downloaded_file
from .message_writer import write_success_message, write_failure_message
from .utilities import load_web_page


def click_browse_receipts_button(driver, locator: tuple, state: str, district: str, first_name: str, last_name: str):
    action = "click browse reciepts button"
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    max_attempts = 5
    for attempt in range(1, max_attempts):
        load_web_page(driver = driver)
        try:
            element_browse_receipts = WebDriverWait(driver = driver, timeout = 30).until(
                EC.element_to_be_clickable(locator = locator)
            )
            driver.execute_script("arguments[0].click();", element_browse_receipts)
            message = write_success_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
            driver.refresh()
            time.sleep(10)
    logging.info(msg = message)
    return False


def click_export_button(driver, locator: tuple, state: str, district: str, first_name: str, last_name: str):
    action = "click export button"
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    max_attempts = 5
    for attempt in range(1, max_attempts):
        load_web_page(driver = driver)
        try:
            element_export_button = WebDriverWait(driver = driver, timeout = 10).until(
                EC.presence_of_element_located(locator = locator)
            )
            driver.execute_script("arguments[0].click();", element_export_button)
            message = write_success_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, exception = e)
            print(message)
            driver.refresh(10)
            time.sleep(10)
    logging.info(msg = message)
    return False


def click_download_button(driver, locator: tuple, state: str, district: str, first_name: str, last_name: str):
    action = "click download button"
    subject = f"{state}-{district} candidate {first_name} {last_name}"
    max_attempts = 10
    for attempt in range(1, max_attempts):
        try:
            load_web_page(driver = driver)
            WebDriverWait(driver = driver, timeout = 30).until(
                EC.presence_of_element_located(locator = locator)
            )
            text_preparing_download = "We're preparing your download"
            WebDriverWait(driver = driver, timeout = 120).until_not(
                EC.text_to_be_present_in_element(
                    locator = locator,
                    text_ = text_preparing_download)
            )
            element_download_button = WebDriverWait(driver = driver, timeout = 30).until(
                EC.element_to_be_clickable(locator = locator)
            )
            print(f"Starting to {action} for {subject}")
            driver.execute_script("arguments[0].click();", element_download_button)
            if find_downloaded_file(subject = subject):
                message = write_success_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                return True
            else:
                time.sleep(5)
                continue
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
    logging.info(msg = message)
    return False
    

def click_close_download_button(driver, locator: tuple, state: str, district: str, first_name: str, last_name: str):

    action = "click close download button"
    subject = f"{state}-{district} candidate {first_name} {last_name}"

    max_attempts = 25
    for attempt in range(1, max_attempts):
        try:
            load_web_page(driver = driver)
            element_close_download_button = WebDriverWait(driver = driver, timeout = 120).until(
                EC.element_to_be_clickable(locator = locator)
            )
            driver.execute_script("arguments[0].click();", element_close_download_button)
            WebDriverWait(driver = driver, timeout = 5).until_not(
                EC.visibility_of_element_located(locator = locator)
            )
            message = write_success_message(action = action, subject = subject)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
    logging.info(message)
    return False


def select_results_per_page(driver, chamber, state, district):

    action = "select results per page"
    if district:
        subject = f"{state}-{district}"
    else:
        subject = f"{state}-{chamber.capitalize()}"

    max_attempts = 25
    for attempt in range(1, max_attempts):
        try:
            load_web_page(driver = driver)
            locator_results_per_page = (By.CSS_SELECTOR, "#DataTables_Table_0_length > label:nth-child(1) > select:nth-child(1)")
            element_results_per_page = WebDriverWait(driver = driver, timeout = 60).until(
                EC.element_to_be_clickable(locator = locator_results_per_page)
            )
            time.sleep(1)
            Select(webelement = element_results_per_page).select_by_value(value = "100")
            message = write_success_message(action = action, subject = subject)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
            print(message)
            driver.refresh()
            time.sleep(10)
    logging.info(message)
    return False