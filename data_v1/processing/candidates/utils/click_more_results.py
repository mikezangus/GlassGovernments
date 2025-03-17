from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def click_more_results(driver: webdriver.Firefox) -> None:
    try:
        selector = "#more-results"
        locator = (By.CSS_SELECTOR, selector)
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(locator)
        )
        element.click()
        print("Clicked more results button")
    except Exception as e:
        print("Failed to click more results button. Error:", e)
    return
