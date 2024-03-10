import os
import pandas as pd
import subprocess
import sys
from selenium import webdriver
from .utils.convert_office_code_to_name import convert_office_code_to_name
from .utils.convert_state_code_to_name import convert_state_code_to_name
from .utils.get_name import get_name
from .utils.open_site import open_site
from .utils.search import search


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSING_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PROCESSING_DIR)
from utils.get_mongo_config import get_mongo_config
from utils.filter_out_existing_items import filter_out_existing_items
from utils.load_df_from_mongo import load_pd_df_from_mongo
from utils.sanitize_df import sanitize_df
from utils.upload_df import upload_df

DATA_DIR = os.path.dirname(PROCESSING_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year
from utils.firefox.load_driver import load_driver


def process_name(driver: webdriver.Firefox, query: str) -> str | None:
    search(driver, query)
    success, site = open_site(driver)
    if success:
        name = get_name(driver, site)
        return name
    return


def process_df(df: pd.DataFrame) -> pd.DataFrame:
    df["NAME"] = None
    fails = []
    for index, row in df.iterrows():
        progress_msg = f"[{(index + 1):,}/{len(df):,}]"
        try:
            driver_loaded, driver = load_driver(True)
            if not driver_loaded:
                return
            state = convert_state_code_to_name(row["STATE"])
            office = convert_office_code_to_name(row["OFFICE"])
            query = f"{row['FEC_NAME']} {state} {office}"
            print(f"\n{progress_msg} {query}")
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


def process_names(year: str = None):
    caffeinate_path = os.path.join(
        DATA_DIR,
        "utils",
        "caffeinate.sh"
    )
    subprocess.run([caffeinate_path, "start"])
    if not year:
        year = decide_year(False)
    output_collection = f"{year}_cands"
    uri, db_name = get_mongo_config()
    input_df = load_pd_df_from_mongo(
        uri,
        db_name,
        f"{year}_cands_raw",
        "Candidate Names"
    )
    print(input_df.head())
    existing_items_df = load_pd_df_from_mongo(
        uri,
        db_name,
        output_collection,
        "Existing Items"
    )
    if existing_items_df is not None:
        print("INPUT DF:")
        print(input_df.head())
        print("EXISTING ITEMS DF:")
        print(existing_items_df.head())
        input_df = filter_out_existing_items(
            input_df,
            existing_items_df,
            "CAND_ID"
        )
        print("FILTERED DF:")
        print(input_df.head())
    if len(input_df) == 0:
        print("No new items to process, exiting")
        return

    main_df = process_df(input_df)
    main_df = sanitize_df(
        "name",
        main_df
    )
    upload_df(
        output_collection,
        uri,
        main_df,
        db_name,
        "overwrite"
    )
    subprocess.run([caffeinate_path, "stop"])
    return


if __name__ == "__main__":
    process_names()
