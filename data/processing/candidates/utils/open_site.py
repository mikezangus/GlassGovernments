from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from .click_more_results import click_more_results


def open_site(driver: webdriver.Firefox) -> tuple[bool, str | None]:
    for i in range(1000):
        try:
            if (i + 1) % 10 == 0:
                click_more_results(driver)
            selector = f"#r1-{i} > div:nth-child(1)"
            locator = (By.CSS_SELECTOR, selector)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            url = element.text
            print(url)
            if "https://ballotpedia.org" in url:
                element.click()
                return True, "ballot"
            elif "https://en.wikipedia.org" in url:
                element.click()
                return True, "wiki"
        except:
            continue
    return False, None
