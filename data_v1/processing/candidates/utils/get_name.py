from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Literal
from .strip_string import strip_string


def get_name(driver: webdriver.Firefox, site: Literal["ballot", "wiki"]) -> str | None:
    for _ in range(15):
        try:
            driver.refresh()
            if site == "ballot":
                selector = "#firstHeading > span:nth-child(1)"
            elif site == "wiki":
                selector = ".mw-page-title-main"
            locator = (By.CSS_SELECTOR, selector)
            element = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(locator)
            )
            name = strip_string(element.text)
            return name
        except Exception as e:
            print(f"Failed to get name from {site}. Error:", e)
            continue
    return
