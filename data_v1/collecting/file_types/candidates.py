import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .utilities import open_pane


def find_election_year(driver: webdriver.Firefox, input_year: str) -> str:
    locator = (
        By.CSS_SELECTOR,
        "#first-content-1 > div:nth-child(3) > ul:nth-child(1)"
    )
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(locator)
    )
    years_items = element.find_elements(By.TAG_NAME, "li")
    for years_item in years_items:
        years = re.findall(r"\d{4}", years_item.text)
        if years and int(years[0]) <= int(input_year) <= int(years[1]):
            election_year = years[1]
    return election_year


def download_main_file(driver: webdriver.Firefox, election_year: str) -> None:
    print("\nStarted downloading main file for Candidates")
    locator = (
        By.CSS_SELECTOR,
        "#first-content-1 > div:nth-child(3) > ul:nth-child(1)"
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


def download_header_file(driver: webdriver.Firefox) -> None:
    print("Started downloading header file for Candidates")
    locator = (
        By.CSS_SELECTOR,
        "p.icon-download--inline--left:nth-child(4) > a:nth-child(1)"
    )
    element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(locator)
    )
    element.click()
    return


def download_candidates(driver: webdriver.Firefox, input_year: str) -> tuple[bool, str]:
    try:
        open_pane(driver, "3")
        election_year = find_election_year(driver, input_year)
        download_main_file(driver, election_year)
        download_header_file(driver)
        return True, election_year
    except Exception as e:
        print("Download Candidates | Error:", e)
        return False, None
