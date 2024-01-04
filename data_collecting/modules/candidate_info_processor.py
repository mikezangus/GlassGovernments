import logging
import re
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modules.sub_modules.message_writer import write_failure_message


def process_candidate_info(driver, subject, elements: list, css_selector_base: str):
    action = "process info"
    try:
        element_full_name, element_party, element_total_receipts = elements
        full_name = element_full_name.split(", ")
        last_name, first_name = full_name[0].rstrip(",").replace(" ", "-"), full_name[1].replace(" ", "-")
        total_receipts = float(re.sub(pattern = "[,$]", repl = "", string = element_total_receipts))
        if total_receipts == 0.00 or 0:
            print(f"Total donation amount: ${total_receipts:,.2f}, moving on")
            return False, None, None, None
        if element_party.lower() == "no party affiliation":
            party = "NO-PARTY-AFFILIATION"
        elif element_party:
            party = element_party.split(" ")[0]
        else:
            party = "NO-PARTY-FOUND"
        locator_candidate_button = (By.CSS_SELECTOR, css_selector_base + "> td:nth-child(1) > a:nth-child(1)")
        element_candidate_button = WebDriverWait(driver, 5).until(EC.presence_of_element_located(locator_candidate_button))
        time.sleep(1)
        driver.execute_script("arguments[0].click();", element_candidate_button)
        start_time = datetime.now()
        print(f"{start_time.strftime('%H:%M:%S')} | Starting to scrape for {first_name} {last_name} ({party})")
        print(f"Total donation amount: ${total_receipts:,.2f}")
        return True, first_name, last_name, party
    except Exception as e:
        message = write_failure_message(action, subject, exception = e, notes = "Possible abnormal naming structure")
        print(message)
        logging.info(message)
    return False, None, None, None