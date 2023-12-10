import logging
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from downloaded_files_manager import prepare_download_path, save_downloaded_file
from scraper_utilities import load_web_page
from message_generator import generate_message


def scrape_one_candidate(driver, year, chamber, state, district, candidate_count, i):


    if district == None:
        district = chamber.upper()
    else:
        district = str(district).zfill(2)

    css_selector_base = f"#DataTables_Table_0 > tbody:nth-child(2) > tr:nth-child({i + 1})"
    css_selectors_candidate = [" > td:nth-child(1)", " > td:nth-child(2)", " > td:nth-child(3)"]
    locator_funding = (By.CSS_SELECTOR, "div.entity__figure--narrow:nth-child(4) > div:nth-child(1)")
    locator_browse_receipts = (By.CSS_SELECTOR, "#total-raised > div:nth-child(1) > a:nth-child(2)")
    locator_data_container = (By.CSS_SELECTOR, ".data-container__action")
    locator_export_button = (By.CSS_SELECTOR, ".js-export.button.button--cta.button--export")
    locator_downloads_pane = (By.CSS_SELECTOR, ".downloads")
    locator_download_button = (By.CSS_SELECTOR, "a.button")
    locator_close_download_button = (By.CSS_SELECTOR, "button.js-close:nth-child(3)")

    max_attempts = 5


    def find_candidate():
        action = "find"
        subject = f"{state}-{district} candidate {i + 1}/{candidate_count}"
        for attempt in range(max_attempts):
            if not load_web_page(driver = driver):
                continue
            elements = []
            for css_selector_candidate in css_selectors_candidate:
                try:
                    locator_candidate = (By.CSS_SELECTOR, css_selector_base + css_selector_candidate)
                    element_candidate = WebDriverWait(driver = driver, timeout = 15).until(
                        EC.presence_of_element_located(locator = locator_candidate)
                    )
                    elements.append(element_candidate.text)
                except Exception as e:
                    message = generate_message(action = action, subject = subject, exception = e, attempt = attempt, max_attempts = max_attempts)
                    print(message)
                    break
            else:
                return True, elements
        else:
            message = generate_message(action = action, subject = subject, attempt = max_attempts, max_attempts = max_attempts)
            print(message)
            logging.info(msg = message)
            return False, None

    
    def process_candidate_info(elements):
        action = "process info"
        subject = f"{state}-{district} candidate {i + 1}/{candidate_count}"
        try:
            element_full_name, element_party, element_total_receipts = elements
            full_name = element_full_name.split(", ")
            last_name, first_name = full_name[0].rstrip(",").replace(" ", "-"), full_name[1].replace(" ", "-")
            total_receipts = float(re.sub("[,$]", "", element_total_receipts))
            if total_receipts == 0:
                print(f"{state}-{district} {i + 1}/{candidate_count}: {first_name} {last_name} received ${total_receipts:,.2f} in donations, moving on")
                return False, None, None, None
            else:
                party = element_party.split(" ")[0] if element_party else "NO-PARTY-FOUND"
                locator_candidate = (By.CSS_SELECTOR, css_selector_base + "> td:nth-child(1) > a:nth-child(1)")
                element_candidate = WebDriverWait(driver = driver, timeout = 15).until(
                    EC.presence_of_element_located(locator = locator_candidate)
                )
                time.sleep(1)
                print(f"{state}-{district} {i + 1}/{candidate_count}: Starting to scrape {first_name} {last_name} ({party}), who received ${total_receipts:,.2f} in donations")
                element_candidate.click()
                return True, first_name, last_name, party
        except Exception as e:
            message = generate_message(action = action, subject = subject, exception = e, notes = "Possible abnormal naming structure")
            print(message)
            logging.info(msg = message)
            return False, None, None, None
                

    def check_if_candidate_has_funding(first_name, last_name):
        action = "check if funding data exists"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        for attempt in range(max_attempts):
            load_web_page(driver = driver)
            try:
                text_funding = WebDriverWait(driver = driver, timeout = 60).until(
                    EC.presence_of_element_located(locator = locator_funding)
                )
                if "we don't have" in text_funding.text.lower():
                    message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                    print(message)
                    if attempt < max_attempts - 1:
                        driver.refresh()
                        time.sleep(5)
                    else:
                        logging.info(msg = message)
                        driver.back()
                        return False
                else:
                    return True
            except Exception as e:
                message = generate_message(action = action, subject = subject, exception = e, attempt = attempt, max_attempts = max_attempts)
                print(message)
                if attempt < max_attempts - 1:
                    driver.refresh()
                    time.sleep(5)
                else:
                    logging.info(msg = message)
                    return False


    def click_browse_receipts_button(first_name, last_name):
        action = "click browse reciepts button"
        subject = f"{state}-{district} candidate {first_name} {last_name}"
        for attempt in range(max_attempts):
            load_web_page(driver = driver)
            try:
                element_browse_receipts = WebDriverWait(driver = driver, timeout = 30).until(
                    EC.element_to_be_clickable(locator = locator_browse_receipts)
                )
                element_browse_receipts.click()
                return True
            except Exception as e:
                message = generate_message(action = action, subject = subject, exception = e, attempt = attempt, max_attempts = max_attempts)
                print(message)
                if attempt < max_attempts - 1:
                    driver.refresh()
                    time.sleep(5)
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
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts, exception = e)
                print(message)
                driver.refresh()
                time.sleep(5)
                if attempt >= max_attempts - 1:
                    logging.info(message)
                    return False
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


    def download_data (first_name, last_name, party):


        def click_export_button():
            try:
                load_web_page(driver = driver)
                element_export_button = WebDriverWait(driver = driver, timeout = 10).until(
                    EC.presence_of_element_located(locator = locator_export_button)
                )
                element_export_button.click()
                return True
            except Exception:
                return False


        def click_download_button():
            try:
                WebDriverWait(driver = driver, timeout = 30).until(
                    EC.presence_of_element_located(locator = locator_downloads_pane)
                )
                text_preparing_download = "We're preparing your download"
                WebDriverWait(driver = driver, timeout = 120).until_not(
                    EC.text_to_be_present_in_element(
                        locator = locator_downloads_pane,
                        text_ = text_preparing_download)
                )
                element_download_button = WebDriverWait(driver = driver, timeout = 30).until(
                    EC.element_to_be_clickable(locator = locator_download_button)
                )
                element_download_button.click()
                return True
            except Exception:
                return False


        def click_close_download_button():
            try:
                element_close_download_button = WebDriverWait(driver = driver, timeout = 30).until(
                    EC.element_to_be_clickable(locator = locator_close_download_button)
                )
                element_close_download_button.click()
                return True
            except Exception:
                return False
            

        def handle_rate_limit():
            rate_limit_wait_time = 30
            try:
                element_downloads_pane = WebDriverWait(driver = driver, timeout = 30).until(
                    EC.presence_of_element_located(locator = locator_downloads_pane)
                )
                text_downloads_pane = element_downloads_pane.text.lower()
                if "exceeded your maximum downloads" in text_downloads_pane.lower():
                    if attempt <= max_download_attempts:
                        time.sleep(rate_limit_wait_time * 60)
                        return
                    else:
                        return False
            except Exception:
                return False
        

        subject = f"{state}-{district} candidate {first_name} {last_name}"


        def process_download_sequence(attempt, max_attempts):
            if not click_export_button():
                action = "click export button"
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                return False
            if not prepare_download_path():
                action = "prepare download path"
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                return False
            if not click_download_button():
                action = "click download button"
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                if not handle_rate_limit():
                    action = "handle rate limit"
                    message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                    print(message)
                    return False
            if not save_downloaded_file(year = year, state = state, district = district, last_name = last_name, first_name = first_name, party = party):
                action = "save downloaded file"
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                return False
            if not click_close_download_button():
                action = "click_close_download_button"
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_attempts)
                print(message)
                return False
            else:
                return True


        action = "download data"
        max_download_attempts = 20
        for attempt in range(max_download_attempts):
            if process_download_sequence(attempt = attempt, max_attempts = max_download_attempts):
                return True
            else:
                message = generate_message(action = action, subject = subject, attempt = attempt, max_attempts = max_download_attempts)
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
    
    browse_receipts_button_clicked = click_browse_receipts_button(first_name = first_name, last_name = last_name)
    if not browse_receipts_button_clicked:
        return
    
    export_available = check_if_export_available(first_name = first_name, last_name = last_name)
    if not export_available:
        return
    
    data_downloaded = download_data(first_name = first_name, last_name = last_name, party = party)
    if not data_downloaded:
        return