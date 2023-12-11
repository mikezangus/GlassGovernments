import logging
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.button_clickers import click_browse_receipts_button, click_export_button, click_download_button, click_close_download_button
from modules.download_manager import prepare_download_path, save_downloaded_file
from modules.element_locators import locator_funding, locator_browse_receipts, locator_data_container, locator_export_button, locator_downloads_pane, locator_download_button, locator_close_download_button
from modules.message_writer import write_failure_message
from modules.utilities import load_base_url, load_web_page, handle_rate_limit


def scrape_one_candidate(driver, year: str, chamber: str, state: str, district: str, candidate_count: str, i: int):

    
    css_selector_base = f"#DataTables_Table_0 > tbody:nth-child(2) > tr:nth-child({i})"
    css_selectors_candidate = [" > td:nth-child(1)", " > td:nth-child(2)", " > td:nth-child(3)"]

    max_attempts = 5

    load_base_url(driver = driver, year = year, chamber = chamber, state = state, district = district)


    def find_candidate():
        action = "find element"
        subject = f"{state}-{district} candidate {i}/{candidate_count}"
        for attempt in range(1, max_attempts):
            load_web_page(driver = driver)
            elements = []
            for css_selector_candidate in css_selectors_candidate:
                try:
                    locator_candidate = (By.CSS_SELECTOR, css_selector_base + css_selector_candidate)
                    element_candidate = WebDriverWait(driver = driver, timeout = 15).until(
                        EC.presence_of_element_located(locator = locator_candidate)
                    )
                    elements.append(element_candidate.text)
                except Exception as e:
                    message = write_failure_message(action = action, subject = subject, exception = e, attempt = attempt, max_attempts = max_attempts)
                    print(message)
                    break
            return True, elements
        message = write_failure_message(action = action, subject = subject, attempt = max_attempts, max_attempts = max_attempts)
        print(message)
        logging.info(msg = message)
        return False, None

    
    def process_candidate_info(elements):
        action = "process info"
        subject = f"{state}-{district} candidate {i}/{candidate_count}"
        try:
            element_full_name, element_party, element_total_receipts = elements
            full_name = element_full_name.split(", ")
            last_name, first_name = full_name[0].rstrip(",").replace(" ", "-"), full_name[1].replace(" ", "-")
            total_receipts = float(re.sub("[,$]", "", element_total_receipts))
            if total_receipts == 0:
                print(f"{state}-{district} candidate {i}/{candidate_count}: {first_name} {last_name} received ${total_receipts:,.2f} in donations, moving on")
                return False, None, None, None
            party = element_party.split(" ")[0] if element_party else "NO-PARTY-FOUND"
            locator_candidate = (By.CSS_SELECTOR, css_selector_base + "> td:nth-child(1) > a:nth-child(1)")
            element_candidate = WebDriverWait(driver = driver, timeout = 15).until(
                EC.presence_of_element_located(locator = locator_candidate)
            )
            time.sleep(1)
            print(f"{state}-{district} candidate {i}/{candidate_count}: Starting to scrape {first_name} {last_name} ({party}), who received ${total_receipts:,.2f} in donations")
            element_candidate.click()
            return True, first_name, last_name, party
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, exception = e, notes = "Possible abnormal naming structure")
            print(message)
            logging.info(msg = message)
        return False, None, None, None
                

    def check_if_candidate_has_funding(first_name, last_name):
        action = "check if funding data exists"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        for attempt in range(1, max_attempts):
            load_web_page(driver = driver)
            try:
                text_funding = WebDriverWait(driver = driver, timeout = 60).until(
                    EC.presence_of_element_located(locator = locator_funding)
                )
                if "we don't have" in text_funding.text.lower():
                    message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                    print(message)
                    if attempt < max_attempts:
                        driver.refresh()
                        time.sleep(5)
                    else:
                        logging.info(msg = message)
                        driver.back()
                    return False
                return True
            except Exception as e:
                message = write_failure_message(action = action, subject = subject, exception = e, attempt = attempt, max_attempts = max_attempts)
                print(message)
                if attempt < max_attempts:
                    driver.refresh()
                    time.sleep(5)
                    continue
                else:
                    logging.info(msg = message)
                return False


    def check_if_export_available(first_name, last_name):
        action = f"check if export is available"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        for attempt in range(max_attempts):
            load_web_page(driver = driver)
            try:
                WebDriverWait(driver = driver, timeout = 30).until(
                    EC.visibility_of_element_located(locator = locator_data_container)
                )
                element_export_button = WebDriverWait(driver = driver, timeout = 10).until(
                    EC.presence_of_element_located(locator = locator_export_button)
                )
                if "is-disabled" not in element_export_button.get_attribute("class"):
                    return True
                time.sleep(5)
            except Exception as e:
                message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
                print(message)
            driver.refresh()
            time.sleep(5) 
        if "is-disabled" in element_export_button.get_attribute("class"):
            message = f"Export button disabled for {subject}, skipping"
            print(message)
            logging.info(message)
            time.sleep(1)
            driver.back()
            time.sleep(1)
            driver.back()
            return False
        elif "This table has no data to export" in driver.page_source:
            message = f"No data to export for {subject}, skipping"
            print(message)
            logging.info(message)
            time.sleep(1)
            driver.back()
            time.sleep(1)
            driver.back()
            return False
        logging.info(message)
        return False


    def download_data (first_name, last_name, party):
 

        def process_download_sequence():
            if not click_export_button(driver = driver, locator = locator_export_button, state = state, district = district, first_name = first_name, last_name = last_name):
                return False
            if not prepare_download_path(state = state, district = district, first_name = first_name, last_name = last_name):
                return False
            if not click_download_button(driver = driver, locator = locator_download_button, state = state, district = district, first_name = first_name, last_name = last_name):
                if not handle_rate_limit(driver = driver, locator = locator_downloads_pane, state = state, district = district, first_name = first_name, last_name = last_name):
                    return False
            if not save_downloaded_file(year = year, state = state, district = district, last_name = last_name, first_name = first_name, party = party):
                return False
            if not click_close_download_button(driver = driver, locator = locator_close_download_button, state = state, district = district, first_name = first_name, last_name = last_name):
                return False
            else:
                return True


        action = "download data"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        max_download_attempts = 20
        for attempt in range(1, max_download_attempts):
            if process_download_sequence():
                return True
            else:
                message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_download_attempts)
                print(message)
                logging.info(msg = message)
                return False

    
    candidate_found, elements = find_candidate()
    if not candidate_found:
        return
    
    candidate_info_proccessed, first_name, last_name, party = process_candidate_info(elements = elements)
    if not candidate_info_proccessed:
        return
    
    candidate_has_funding = check_if_candidate_has_funding(first_name = first_name, last_name = last_name)
    if not candidate_has_funding:
        return
    
    browse_receipts_button_clicked = click_browse_receipts_button(driver = driver, locator = locator_browse_receipts, state = state, district = district, first_name = first_name, last_name = last_name)
    if not browse_receipts_button_clicked:
        return
    
    export_available = check_if_export_available(first_name = first_name, last_name = last_name)
    if not export_available:
        return
    
    data_downloaded = download_data(first_name = first_name, last_name = last_name, party = party)
    if not data_downloaded:
        return