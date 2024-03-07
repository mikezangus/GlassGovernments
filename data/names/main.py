import os
import pandas as pd
import re
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from typing import Literal

from get_mongo_info import get_mongo_info
from load_df_from_mongo import load_df_from_mongo
from upload_df_to_mongo import upload_df_to_mongo
from firefox.firefox_driver import main as load_firefox_driver

current_dir = os.path.dirname(__file__)
data_dir = os.path.dirname(current_dir)
sys.path.append(data_dir)
from geography.usa.states.usa_state_loader import load_full_file


def strip_string(input: str) -> str:
    output = re.sub(
        r'\s*\([^)]*\)',
        "",
        input
    )
    return output


def search(driver: webdriver.Firefox, query: str) -> None:
    url = f"https://duckduckgo.com/?q={query}"
    driver.get(url)
    return


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
    return None


def process_name(driver: webdriver.Firefox, query: str) -> str | None:
    search(driver, query)
    success, site = open_site(driver)
    if success:
        name = get_name(driver, site)
        return name
    return


def convert_state_code_to_name(state_code: str) -> str:
    states_dict = load_full_file()
    reverse_states_dict = {
        v: k for k, v in states_dict.items()
    }
    state_name = reverse_states_dict.get(state_code, "")
    return state_name


def convert_office_code_to_name(chamber_code: str) -> str:
    offices__dict = {
        "H": "Congress",
        "S": "Senate"
    }
    office = offices__dict.get(chamber_code, "")
    return office


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    df["NAME"] = None
    fails = []
    for index, row in df.iterrows():
        progress_msg = f"[{(index + 1):,}/{len(df):,}]"
        try:
            driver_loaded, driver = load_firefox_driver(True)
            if not driver_loaded:
                return
            state = convert_state_code_to_name(row["STATE"])
            office = convert_office_code_to_name(row["OFFICE"])
            query = f"{row['FEC_NAME']} {state} {office}"
            print("")
            print(progress_msg, query)
            name = process_name(driver, query)
            if name is not None:
                print(progress_msg, f"{row['FEC_NAME']} -> {name}")
                df.at[index, "NAME"] = name
            else:
                print(progress_msg, f"{row['FEC_NAME']} -> failed to find name")
                df.at[index, "NAME"] = "None"
                fails.append(query)
            driver.quit()
        except Exception as e:
            print(progress_msg, "Error:", e)
            continue
    print("Fails:\n", fails)
    return df


def main():
    caffeinate_path = os.path.join(current_dir, "caffeinate.sh")
    subprocess.run([caffeinate_path, "start"])
    year = "2024"
    uri, db = get_mongo_info()
    input_df = load_df_from_mongo(uri, db, f"{year}_cands_raw")
    df = process_df(input_df)
    print(df.head())
    upload_df_to_mongo(uri, db, f"{year}_cands", df)
    subprocess.run([caffeinate_path, "stop"])
    return


if __name__ == "__main__":
    main()
