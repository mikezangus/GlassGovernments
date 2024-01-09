import sys
import os
from scraper import scrape_constituency
from firefox.firefox_driver import firefox_driver
from modules.sub_modules.log_creator import create_log_file

collecting_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(collecting_dir)
sys.path.append(data_dir)
from caffeinate import start_caffeinate, stop_caffeinate
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    caffeinate = start_caffeinate()
    try:
        driver_loaded, driver = firefox_driver()
        if not driver_loaded:
            print("\nQuitting data collection driver\n")
            return
        else:
            driver.quit()
        constituency_list = get_user_inputs("scrape", "internet")
        print(f"\nConstituency list via data collection driver:\n{constituency_list}")
        create_log_file()
        completed_state = None
        for constituency in constituency_list:
            year, chamber, state = constituency.split("_")[:3]
            if state == completed_state:
                continue
            if chamber.lower() == "house":
                district = constituency.split("_")[3]
            elif chamber.lower() == "senate":
                district = None
            if not scrape_constituency("scrape", year, chamber, state, district):
                completed_state = state
                continue
    except Exception as e:
        print(f"\nFailed to scrape inputted data. Exception: {e}")
    finally:
        stop_caffeinate(caffeinate)
        print(f"\nFinished scraping inputted data")
        print("\nQuitting data collecting driver\n")


if __name__ == "__main__":
    main()