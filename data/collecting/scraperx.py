import os
import sys
import time
from modules.load_spark import load_spark
from modules.get_mongo_uri import get_mongo_uri
from modules.load_df_from_mongo import load_df_from_mongo
from modules.decide_year import decide_year
from firefox.firefox_driver import firefox_driver
from pyspark.sql import DataFrame
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from datetime import datetime, timedelta


collecting_dir = os.path.dirname(__file__)
data_dir = os.path.dirname(collecting_dir)
sys.path.append(data_dir)
from directories import get_raw_dir


def convert_df_to_list(df: DataFrame) -> list:
    list = [row["CMTE_ID"] for row in df.collect()]
    return list


def load_url(driver: webdriver.Firefox, cmte_id: str, election_year: str) -> None:
    election_year_minus_two = int(election_year) - 2
    url = f"https://www.fec.gov/data/receipts/?committee_id={cmte_id}&two_year_transaction_period={election_year}&two_year_transaction_period={election_year_minus_two}&line_number=F3-12&data_type=processed"
    driver.get(url)
    return


def load_web_page(driver: webdriver.Firefox):
    for _ in range(5):
        try:
            WebDriverWait(driver, 60).until(
                lambda d: d.execute_script("return jQuery.active==0")
            )
            WebDriverWait(driver, 60).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except Exception as e:  
            driver.refresh()
    return False


def verify_export_available(driver: webdriver.Firefox) -> bool:
    load_web_page(driver)
    locator = (By.CSS_SELECTOR, ".js-count")
    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(locator)
    )
    message = element.text.lower()
    print("Donation count:", message)
    if "0" in message:
        return False
    return True


def click_export_button(driver: webdriver.Firefox) -> bool:
    locator = (By.CSS_SELECTOR, ".data-container__export")
    for _ in range(10):
        try:
            load_web_page(driver)
            if not verify_export_available(driver):
                return False
            element = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            return True
        except Exception:
            driver.refresh()
            time.sleep(10)
    return False


def find_downloaded_file(dir: str) -> bool:
    if os.listdir(dir):
        return True
    print("No file found")
    return False


def handle_rate_limit(driver: webdriver.Firefox, element: WebElement) -> None:
    wait_time_minutes = 30
    text_downloads_pane = element.text
    if "maximum downloads" in text_downloads_pane.lower() or "server error" in text_downloads_pane.lower():
        current_time = datetime.now()
        end_time = current_time + timedelta(minutes = wait_time_minutes)
        print(f"Rate limit hit at {current_time.strftime('%H:%M:%S')}, trying again in {wait_time_minutes} minutes at {end_time.strftime('%H:%M:%S')}")
        time.sleep(wait_time_minutes * 60)
        resume_time = datetime.now()
        print(f"Rate limit wait over at {resume_time.strftime('%H:%M:%S')}, refreshing page and trying again")
        driver.refresh()
        return


def click_download_button(driver: webdriver.Firefox, dir: str) -> bool:
    locator_pane = (By.CSS_SELECTOR, ".downloads")
    locator_button = (By.CSS_SELECTOR, "a.button")
    for _ in range(10):
        try:
            load_web_page(driver)
            element_pane = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(locator_pane)
            )
            WebDriverWait(driver, 120).until_not(
                EC.text_to_be_present_in_element(
                    locator_pane, "preparing your download"
                )
            )
            element_button = WebDriverWait(driver, 120).until(
                EC.element_to_be_clickable(locator_button)
            )
            element_button.click()
            time.sleep(1)
            if find_downloaded_file(dir):
                return True
        except Exception:
            handle_rate_limit(driver, element_pane)
    return False


def handle_export_and_download(driver: webdriver.Firefox, dir: str) -> bool:
    for _ in range(5):
        if not click_export_button(driver):
            continue
        elif not click_download_button(driver, dir):
            continue
        return True
    return False


def scrape_one_candidate(driver: webdriver.Firefox, year: str, candidate: str, dir) -> bool:
    load_url(driver, candidate, year)
    if not handle_export_and_download(driver, dir):
        return False
    return True
    

def candidate_loop(list: list, year: str) -> None:
    for i, candidate in enumerate(list):
        dir = os.path.join(get_raw_dir(), year, "transfers", candidate)
        driver_loaded, driver = firefox_driver(dir)
        if not driver_loaded:
            print("Driver failed to load")
            continue
        print(f"[{i + 1}/{len(list)}] | Started scraping for {candidate}")
        if scrape_one_candidate(driver, year, candidate, dir):
            print(f"[{i + 1}/{len(list)}] | Succeeded scraping for {candidate}")
        else:
            print(f"[{i + 1}/{len(list)}] | Failed scraping for {candidate}")
        driver.quit()
    return


def main():
    year = "2024"
    uri = get_mongo_uri()
    spark = load_spark(uri)
    candidates_df = load_df_from_mongo(spark, uri, f"{year}_candidates", "CMTE_ID", subject = "Candidates")
    candidates_df.show()
    candidate_list = convert_df_to_list(candidates_df)
    candidate_loop(candidate_list, year)
    


if __name__ == "__main__":
    main()