import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait



def open_pane(driver: webdriver.Firefox, css_id: str):
    locator = (
        By.CSS_SELECTOR,
        f"button.js-accordion-trigger:nth-child({css_id})"
    )
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(locator)
    )
    status = element.get_attribute("aria-expanded")
    if status.lower() == "false":
        element.click()
    return


def download_main_file(subject, css_id: str, driver: webdriver.Firefox, election_year: str):
    print("\nStarted downloading main file for", subject)
    locator = (
        By.CSS_SELECTOR,
        f"#first-content-{css_id} > div:nth-child(2) > ul:nth-child(1)"
    )
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(locator)
    )
    years_list_items = element.find_elements(By.TAG_NAME, "li")
    for years_list_item in years_list_items:
        years_text = years_list_item.text
        years = re.findall(r"\d{4}", years_text)
        if years and election_year == str(years[1]):
            years_link = years_list_item.find_element(By.TAG_NAME, "a")
            years_link.click()
            break
    return


def download_header_file(subject, css_id: str, driver: webdriver.Firefox):
    print("Started downloading header file for", subject)
    locator = (
        By.CSS_SELECTOR,
        f"#first-content-{css_id} > p:nth-child(3) > a:nth-child(1)"
    )
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()
    return
