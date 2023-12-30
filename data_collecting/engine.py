import logging

from modules.candidate_finder import find_candidate
from modules.candidate_info_processor import process_candidate_info
from modules.candidate_funding_verifier import verify_candidate_has_funding
from modules.export_availability_verifier import verify_export_available
from modules.sub_modules.button_clickers import select_results_per_page, click_browse_receipts_button, click_export_button, click_download_button, click_close_download_button
from modules.sub_modules.download_manager import clear_downloads_container, save_downloaded_file
from modules.sub_modules.element_locators import locator_funding, locator_browse_receipts_button, locator_data_container, locator_donation_count, locator_export_message, locator_export_button, locator_downloads_pane, locator_download_button, locator_close_download_button
from modules.sub_modules.message_writer import write_start_message, write_success_message, write_failure_message
from modules.sub_modules.web_utilities import load_base_url


def scrape_one_candidate(driver, subject, year: str, chamber: str, state: str, candidate: int, district: str = None):
    action = "scrape"
    css_selector_base = f"#DataTables_Table_0 > tbody:nth-child(2) > tr:nth-child({candidate})"
    css_selectors_candidate = [" > td:nth-child(1)", " > td:nth-child(2)", " > td:nth-child(3)"]
    max_attempts = 5
    for attempt in range(max_attempts):
        start_message = write_start_message(action, subject, attempt, max_attempts)
        print(f"{'-' * 100}\n{start_message}")
        load_base_url(driver, subject, year, state, district)
        if candidate > 9:
            select_results_per_page(driver, subject)
        candidate_found, elements = find_candidate(driver, subject, css_selectors_candidate, css_selector_base)
        if not candidate_found:
            continue
        candidate_info_processed, first_name, last_name, party = process_candidate_info(driver, subject, elements, css_selector_base)
        subject = subject + f" {first_name} {last_name}"
        if not district:
            district = chamber.upper()
        if not candidate_info_processed:
            continue
        elif not verify_candidate_has_funding(driver, subject, locator_funding):
            continue
        elif not click_browse_receipts_button(driver, subject, locator_browse_receipts_button):
            continue
        elif not verify_export_available(driver, subject, locator_data_container, locator_donation_count, locator_export_message, locator_export_button):
            continue
        elif not click_export_button(driver, subject, locator_export_button):
            continue
        elif not clear_downloads_container():
            continue
        elif not click_download_button(driver, subject, locator_downloads_pane, locator_download_button):
            continue
        elif not save_downloaded_file(subject, year, chamber, state, district, last_name, first_name, party):
            continue
        elif not click_close_download_button(driver, subject, locator_close_download_button):
            continue
        else:
            success_message = write_success_message(action, subject, attempt, max_attempts)
            print(f"{success_message}\n{'-' * 100}")
            return True
    failure_message = write_failure_message(action, subject, attempt, max_attempts)
    print(f"{failure_message}\n{'-' * 100}")
    logging.info(failure_message)
    return False