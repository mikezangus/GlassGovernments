import sys
import os
from scraper import scrape_constituency
from modules.sub_modules.log_creator import create_log_file

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from caffeinate import start_caffeinate, stop_caffeinate
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    user_inputs_list = get_user_inputs("scrape", "internet")
    print(f"User inputs list via data collection driver:\n{user_inputs_list}")
    caffeinate_process = start_caffeinate()
    try:
        create_log_file()
        current_state = None
        for constituency in user_inputs_list:
            year, chamber, state = constituency.split("_")[:3]
            if chamber.lower() == "house":
                district = constituency.split("_")[3]
            elif chamber.lower() == "senate":
                district = None
            if state != current_state:
                current_state = state
                constituency_exists = True
            constituency_exists, driver_not_loaded = scrape_constituency("scrape", year, chamber, state, district)
            if driver_not_loaded:
                return
            elif not constituency_exists:
                continue
    finally:
        stop_caffeinate(caffeinate_process)


if __name__ == "__main__":
    main()