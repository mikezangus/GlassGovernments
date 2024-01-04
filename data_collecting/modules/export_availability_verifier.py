import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modules.sub_modules.element_locators import locator_data_container, locator_donation_count, locator_export_message, locator_export_button
from modules.sub_modules.message_writer import write_success_message
from modules.sub_modules.web_utilities import load_web_page


def get_donation_count(driver):
    for _ in range(5):
        try:
            element_donation_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator_donation_count))
            donation_count = int(element_donation_count.text.replace(",", ""))
            if donation_count > 100000000:
                driver.refresh()
                time.sleep(5)
                continue
            elif donation_count == 0:
                print(f"Total donation count: 0")
                return False, None
            else:
                print(f"Total donation count: {donation_count:,}")
                return True, donation_count
        except Exception:
            continue
    print(f"Failed to get donation count")
    return False, None


def read_export_message(driver, subject, donation_count: int):
    export_message = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator_export_message)).text.lower()
    if "no data to export" in export_message:
        message = f"No data to export for {subject}"
        print(message)
        logging.info(message)
        return False
    elif donation_count >= 500000 and "bulk data" in export_message:
        message = f"{subject}'s data needs to be downloaded at:\nhttps://www.fec.gov/data/browse-data/?tab=bulk-data"
        print(message)
        logging.info(message)
        return False
    return True


def verify_export_button_enabled(driver, subject):
    element_export_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator_export_button))
    if "is-disabled" in element_export_button.get_attribute("class"):
        message = f"Export button disabled for {subject}, moving on"
        print(message)
        logging.info(message)
        return False
    return True


def verify_export_available(driver, subject):
    action = "verify that export is available"
    load_web_page(driver, subject)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator_data_container))
    success, donation_count = get_donation_count(driver)
    if not success:
        return False
    elif not read_export_message(driver, subject, donation_count):
        return False
    elif not verify_export_button_enabled(driver, subject):
        return False
    message = write_success_message(action, subject)
    print(message)
    return True