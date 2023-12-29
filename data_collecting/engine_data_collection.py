import logging
import re
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from modules.button_clickers import click_browse_receipts_button, click_export_button, click_download_button, click_close_download_button
from modules.download_manager import clear_downloads_container, save_downloaded_file
from modules.element_locators import locator_funding, locator_browse_receipts, locator_data_container, locator_donation_count, locator_export_button, locator_export_message, locator_downloads_pane, locator_download_button, locator_close_download_button
from modules.message_writer import write_failure_message, write_success_message
from modules.web_utilities import load_web_page


def scrape_one_candidate(driver, year: str, chamber: str, state: str, district: str, candidate_count: str, candidate: int):


    css_selector_base = f"#DataTables_Table_0 > tbody:nth-child(2) > tr:nth-child({candidate})"
    css_selectors_candidate = [" > td:nth-child(1)", " > td:nth-child(2)", " > td:nth-child(3)"]


    def find_candidate():
        action = "find element"
        subject = f"{state}-{district} candidate {candidate}/{candidate_count}"
        max_attempts = 5
        for attempt in range(max_attempts):
            load_web_page(driver = driver)
            elements = []
            for css_selector_candidate in css_selectors_candidate:
                locator_candidate = (By.CSS_SELECTOR, css_selector_base + css_selector_candidate)
                element_candidate = WebDriverWait(driver = driver, timeout = 15).until(
                    EC.presence_of_element_located(locator = locator_candidate)
                )
                elements.append(element_candidate.text)
            return True, elements
        message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
        print(message)
        logging.info(message)
        return False, None

    
    def process_candidate_info(elements):
        action = "process info"
        subject = f"{state}-{district} candidate {candidate}/{candidate_count}"
        try:
            element_full_name, element_party, element_total_receipts = elements
            full_name = element_full_name.split(", ")
            last_name, first_name = full_name[0].rstrip(",").replace(" ", "-"), full_name[1].replace(" ", "-")
            total_receipts = float(re.sub(pattern = "[,$]", repl = "", string = element_total_receipts))
            if total_receipts == 0.00 or 0:
                print(f"Total donation amount: ${total_receipts:,.2f}, moving on")
                return False, None, None, None
            party = element_party.split(" ")[0] if element_party else "NO-PARTY-FOUND"
            locator_candidate_button = (By.CSS_SELECTOR, css_selector_base + "> td:nth-child(1) > a:nth-child(1)")
            element_candidate_button = WebDriverWait(driver = driver, timeout = 15).until(
                EC.presence_of_element_located(locator = locator_candidate_button)
            )
            time.sleep(1)
            driver.execute_script("arguments[0].click();", element_candidate_button)
            start_time = datetime.now()
            print(f"{'-' * 100}\n{state}-{district} candidate {candidate}/{candidate_count}:\n{start_time.strftime('%H:%M:%S')} | Starting to scrape for {first_name} {last_name} ({party})")
            print(f"Total donation amount: ${total_receipts:,.2f}")
            return True, first_name, last_name, party
        except Exception as e:
            message = write_failure_message(action = action, subject = subject, exception = e, notes = "Possible abnormal naming structure")
            print(message)
            logging.info(message)
        return False, None, None, None
                

    def verify_candidate_has_funding(first_name, last_name):
        action = "verify funding data exists"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        max_attempts = 5
        for attempt in range(max_attempts):
            try:
                WebDriverWait(driver = driver, timeout = 60).until(
                    EC.url_contains("candidate")
                )
                load_web_page(driver = driver)
                text_funding = WebDriverWait(driver = driver, timeout = 60).until(
                    EC.presence_of_element_located(locator = locator_funding)
                )
                if "we don't have" not in text_funding.text.lower():
                    return True
                message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                driver.refresh()
                time.sleep(5)
            except Exception as e:
                message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
                print(message)
                driver.refresh()
                time.sleep(5)
        logging.info(message)
        return False


    def verify_export_available(first_name, last_name):
        action = "verify that export is available"
        subject = f"{state}-{district} candidate {candidate}/{candidate_count} {first_name} {last_name}"
        max_attempts = 10
        for _ in range(max_attempts):

            load_web_page(driver = driver)
            WebDriverWait(driver = driver, timeout = 30).until(
                EC.visibility_of_element_located(locator = locator_data_container)
            )

            element_donation_count = WebDriverWait(driver = driver, timeout = 10).until(
                EC.presence_of_element_located(locator = locator_donation_count)
            )
            donation_count = int(element_donation_count.text.replace(",", ""))
            if donation_count > 100000000:
                driver.refresh()
                continue
            elif donation_count == 0:
                print(f"Total donation count: {donation_count}, moving on")
                return False
            print(f"Total donation count: {donation_count:,}")

            export_message = WebDriverWait(driver = driver, timeout = 30).until(
                EC.presence_of_element_located(locator = locator_export_message)
            ).text.lower()
            if "no data to export" in export_message:
                message = f"No data to export for {subject}, moving on"
                print(message)
                logging.info(message)
                return False
            elif donation_count >= 500000 and "bulk data" in export_message:
                message = f"{subject}'s data needs to be downloaded at https://www.fec.gov/data/browse-data/?tab=bulk-data"
                print(message)
                logging.info(message)
                return False
            
            element_export_button = WebDriverWait(driver = driver, timeout = 10).until(
                EC.presence_of_element_located(locator = locator_export_button)
            )
            if "is-disabled" in element_export_button.get_attribute("class"):
                message = f"Export button disabled for {subject}, moving on"
                print(message)
                logging.info(message)
                return False
            elif "is-disabled" not in element_export_button.get_attribute("class"):
                return True
            
        message = write_failure_message(action = action, subject = subject)
        print(message)
        logging.info(message)
        return False


    def download_data (first_name, last_name, party):


        def process_download_sequence():
            if not click_export_button(driver = driver, locator = locator_export_button, state = state, district = district, first_name = first_name, last_name = last_name):
                return False
            clear_downloads_container()
            if not click_download_button(driver = driver, locator_pane = locator_downloads_pane, locator_button = locator_download_button, state = state, district = district, first_name = first_name, last_name = last_name):
                return False
            elif not save_downloaded_file(year = year, chamber = chamber, state = state, district = district, last_name = last_name, first_name = first_name, party = party):
                return False
            elif not click_close_download_button(driver = driver, locator = locator_close_download_button, state = state, district = district, first_name = first_name, last_name = last_name):
                return False
            return True


        action = "download data"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        max_download_attempts = 20
        for attempt in range(max_download_attempts):
            if process_download_sequence():
                return True
            else:
                message = write_failure_message(action = action, subject = subject, attempt = attempt, max_attempts = max_download_attempts)
                print(message)
        logging.info(message)
        return False


    def main():

        candidate_found, elements = find_candidate()
        if not candidate_found:
            return False
        
        candidate_info_proccessed, first_name, last_name, party = process_candidate_info(elements = elements)
        if not candidate_info_proccessed:
            return False
        
        candidate_has_funding = verify_candidate_has_funding(first_name = first_name, last_name = last_name)
        if not candidate_has_funding:
            return False
        
        browse_receipts_button_clicked = click_browse_receipts_button(driver = driver, locator = locator_browse_receipts, state = state, district = district, first_name = first_name, last_name = last_name)
        if not browse_receipts_button_clicked:
            return False
        
        export_available = verify_export_available(first_name = first_name, last_name = last_name)
        if not export_available:
            return False
        
        data_downloaded = download_data(first_name = first_name, last_name = last_name, party = party)
        if not data_downloaded:
            return False
        
        end_time = datetime.now()
        action = "scrape"
        subject = f"{first_name} {last_name} ({party})"
        message = f"{end_time.strftime('%H:%M:%S')} | {write_success_message(action = action, subject = subject)}\n{'-' * 100}"
        print(message)
        return True
    

    if main():
        return True
    return False