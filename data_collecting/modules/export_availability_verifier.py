import logging
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modules.sub_modules.message_writer import write_success_message
from modules.sub_modules.web_utilities import load_web_page


def get_donation_count(driver, locator: str):
    element_donation_count = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    donation_count = int(element_donation_count.text.replace(",", ""))
    if donation_count > 100000000:
        driver.refresh()
        return False, None
    elif donation_count == 0:
        print(f"Total donation count is 0")
        return False, None
    print(f"Total donation count: {donation_count:,}")
    return True, donation_count


def read_export_message(driver, subject, locator: str, donation_count: int):
    export_message = WebDriverWait(driver, 30).until(EC.presence_of_element_located(locator)).text.lower()
    if "no data to export" in export_message:
        message = f"No data to export for {subject}, moving on"
        print(message)
        logging.info(message)
        return False
    elif donation_count >= 500000 and "bulk data" in export_message:
        message = f"{subject}'s data needs to be downloaded at:\nhttps://www.fec.gov/data/browse-data/?tab=bulk-data"
        print(message)
        logging.info(message)
        return False
    return True


def verify_export_button_enabled(driver, subject, locator: str):
    element_export_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located(locator))
    if "is-disabled" in element_export_button.get_attribute("class"):
        message = f"Export button disabled for {subject}, moving on"
        print(message)
        logging.info(message)
        return False
    return True


def verify_export_available(driver, subject, locator_data_container: str, locator_donation_count: str, locator_export_message: str, locator_export_button: str):
    action = "verify that export is available"
    load_web_page(driver, subject)
    WebDriverWait(driver, 30).until(EC.visibility_of_element_located(locator_data_container))
    success, donation_count = get_donation_count(driver, locator_donation_count)
    if not success:
        return False
    elif not read_export_message(driver, subject, locator_export_message, donation_count):
        return False
    elif not verify_export_button_enabled(driver, subject, locator_export_button):
        return False
    message = write_success_message(action, subject)
    print(message)
    return True