import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from modules.sub_modules.web_utilities import load_web_page
from modules.sub_modules.message_writer import write_success_message, write_failure_message


def find_candidate(driver, subject, css_selectors_candidate: list, css_selector_base: str):
    action = "find element"
    max_attempts = 5
    for attempt in range(max_attempts):
        load_web_page(driver, subject)
        elements = []
        for css_selector_candidate in css_selectors_candidate:
            locator_candidate = (By.CSS_SELECTOR, css_selector_base + css_selector_candidate)
            element_candidate = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located(locator = locator_candidate)
            )
            elements.append(element_candidate.text)
        message = write_success_message(action, subject, attempt, max_attempts)
        print(message)
        return True, elements
    message = write_failure_message(action, subject, attempt, max_attempts)
    print(message)
    logging.info(message)
    return False, None