import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait
from .download_manager import find_downloaded_file
from .message_writer import write_success_message, write_failure_message
from .web_utilities import load_web_page, handle_rate_limit


max_attempts = 5


def click_browse_receipts_button(driver, subject, locator: tuple):
    action = "click browse reciepts button"
    for attempt in range(max_attempts):
        load_web_page(driver, subject)
        try:
            element_browse_receipts = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].click();", element_browse_receipts)
            WebDriverWait(driver, 60).until(EC.url_contains("receipts"))
            message = write_success_message(action, subject, attempt, max_attempts)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action, subject, attempt, max_attempts, e)
            print(message)
            driver.refresh()
            time.sleep(10)
    message = write_failure_message(action, subject, attempt, max_attempts)
    logging.info(message)
    return False


def click_export_button(driver, subject, locator: tuple):
    action = "click export button"
    for attempt in range(max_attempts):
        load_web_page(driver, subject)
        try:
            element_export_button = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].click();", element_export_button)
            message = write_success_message(action, subject, attempt, max_attempts)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action, subject, attempt, max_attempts, e)
            print(message)
            driver.refresh(10)
            time.sleep(10)
    message = write_failure_message(action, subject, attempt, max_attempts)
    logging.info(message)
    return False


def click_download_button(driver, subject, locator_downloads_pane: tuple, locator_download_button: tuple):
    action = "click download button"
    try:
        load_web_page(driver, subject)
        element_downloads_pane = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator_downloads_pane))
        text_preparing_download = "preparing your download"
        WebDriverWait(driver, 120).until_not(EC.text_to_be_present_in_element(locator_downloads_pane, text_preparing_download))
        try:
            element_download_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable(locator_download_button))
            print(f"Started to {action} for {subject}")
            driver.execute_script("arguments[0].click();", element_download_button)
            time.sleep(1)
            if find_downloaded_file():
                return True
        except Exception:
            handle_rate_limit(driver, element_downloads_pane)
    except Exception as e:
        message = write_failure_message(action, subject, None, None, e)
        print(message)
        logging.info(message)
        driver.refresh()
        time.sleep(5)
    return False
    

def click_close_download_button(driver, subject, locator: tuple):
    action = "click close download button"
    for attempt in range(max_attempts):
        try:
            load_web_page(driver, subject)
            element_close_download_button = WebDriverWait(driver, 120).until(EC.element_to_be_clickable(locator))
            driver.execute_script("arguments[0].click();", element_close_download_button)
            WebDriverWait(driver, 5).until_not(EC.visibility_of_element_located(locator))
            message = write_success_message(action, subject, attempt, max_attempts)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action, subject, attempt, max_attempts, e)
            print(message)
    message = write_failure_message(action, subject, attempt, max_attempts)
    logging.info(message)
    return False


def select_results_per_page(driver, subject):
    action = "select results per page"
    for attempt in range(max_attempts):
        try:
            load_web_page(driver, subject)
            locator_results_per_page = (By.CSS_SELECTOR, "#DataTables_Table_0_length > label:nth-child(1) > select:nth-child(1)")
            element_results_per_page = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(locator_results_per_page))
            time.sleep(1)
            Select(element_results_per_page).select_by_value("100")
            message = write_success_message(action, subject, attempt, max_attempts)
            print(message)
            return True
        except Exception as e:
            message = write_failure_message(action, subject, attempt, max_attempts, e)
            print(message)
            driver.refresh()
            time.sleep(10)
    message = write_failure_message(action, subject, attempt, max_attempts)
    logging.info(message)
    return False