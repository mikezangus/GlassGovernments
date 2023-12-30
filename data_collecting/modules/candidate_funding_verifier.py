import logging
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modules.sub_modules.web_utilities import load_web_page
from modules.sub_modules.message_writer import write_success_message, write_failure_message


def verify_candidate_has_funding(driver, subject, locator: str):
    action = "verify funding data exists"
    max_attempts = 5
    for attempt in range(max_attempts):
        try:
            WebDriverWait(driver, 60).until(EC.url_contains("candidate"))
            load_web_page(driver, subject)
            text_funding = WebDriverWait(driver, 60).until(EC.presence_of_element_located(locator))
            if "we don't have" not in text_funding.text.lower():
                message = write_success_message(action, subject, attempt, max_attempts)
                return True
            message = write_failure_message(action, subject, attempt, max_attempts)
            print(message)
            driver.refresh()
            time.sleep(5)
        except Exception as e:
            message = write_failure_message(action, subject, attempt, max_attempts, e)
            print(message)
            driver.refresh()
            time.sleep(5)
    logging.info(message)
    return False