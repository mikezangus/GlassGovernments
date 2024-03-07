import pandas as pd
import re
from get_mongo_info import get_mongo_info
from load_df_from_mongo import load_df_from_mongo
from upload_df_to_mongo import upload_df_to_mongo
from firefox.firefox_driver import main as load_firefox_driver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from typing import Literal
import os
import sys

current_idr = os.path.dirname(__file__)
data_dir = os.path.dirname(current_idr)
sys.path.append(data_dir)

from geography.usa.states.usa_state_loader import load_full_file


def strip_string(input: str):
    output = re.sub(
        r'\s*\([^)]*\)',
        "",
        input
    )
    return output


def search(driver: webdriver.Firefox, query: str):
    url = f"https://duckduckgo.com/?q={query}"
    driver.get(url)
    return


def open_site(driver: webdriver.Firefox) -> tuple[bool, str | None]:
    for i in range(50):
        try:
            if (i + 1) % 10 == 0:
                results_selector = "#more-results"
                results_locator = (By.CSS_SELECTOR, results_selector)
                results_element = WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located(results_locator)
                )
                results_element.click()
                print("Clicked more results")
            selector = f"#r1-{i} > div:nth-child(1)"
            locator = (By.CSS_SELECTOR, selector)
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located(locator)
            )
            url = element.text
            print(url)
            if "wikipedia.org" in url:
                element.click()
                return True, "wiki"
            elif "ballotpedia.org" in url:
                element.click()
                return True, "ballot"
        except:
            continue
    return False, None


def find_name(driver: webdriver.Firefox, site: Literal["wiki", "ballot"]) -> str:
    for attempt in range(15):
        driver.refresh()
        if attempt > 0:
            print(f"Attempt to find name on {site} {attempt + 1}/15")
        if site == "wiki":
            selector = ".mw-page-title-main"
        elif site == "ballot":
            selector = "#firstHeading > span:nth-child(1)"
        locator = (By.CSS_SELECTOR, selector)
        element = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(locator)
        )
        name = strip_string(element.text)
        return name
    return None


def process(driver: webdriver.Firefox, query: str) -> str | None:
    search(driver, query)
    success, site = open_site(driver)
    if success:
        name = find_name(driver, site)
    return name


def get_state_name(state_code: str) -> str:
    states_dict = load_full_file()
    reverse_states_dict = {
        v: k for k, v in states_dict.items()
    }
    state_name = reverse_states_dict.get(state_code, "")
    return state_name


def get_chamber(chamber_letter: str) -> str:
    chambers_dict = {
        "H": "Congress",
        "S": "Senate"
    }
    chamber = chambers_dict.get(chamber_letter, "")
    return chamber


def loop(df: pd.DataFrame) -> pd.DataFrame:
    df["NAME"] = None
    for index, row in df.iterrows():
        success, driver = load_firefox_driver(True)
        if not success:
            return
        state = get_state_name(row["STATE"])
        chamber = get_chamber(row["OFFICE"])
        query = f"{row['FEC_NAME']} {state} {chamber}"
        print(f"\n[{(index + 1):,}/{len(df):,}] {row['FEC_NAME']}")
        name = process(driver, query)
        if name is not None:
            print(f"[{(index + 1):,}/{len(df):,}] {row['FEC_NAME']} -> {name}")
            df.at[index, "NAME"] = name
        else:
            print(f"[{(index + 1):,}/{len(df):,}] {row['FEC_NAME']} -> couldn't find")

        driver.quit()
    return df


def main():
    year = "2024"
    uri, db = get_mongo_info()
    input_df = load_df_from_mongo(uri, db, f"{year}_cands_raw")
    print(input_df.head())
    x_df = input_df.head(5)
    df = loop(input_df)
    print(df.head())
    upload_df_to_mongo(uri, db, f"{year}_cands", df)
    return

main()