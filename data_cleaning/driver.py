import os
import sys
from engine import clean_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from caffeinate import start_caffeinate, stop_caffeinate
from project_directories import load_data_dir, load_raw_data_dir
from user_inputs.driver_user_inputs import get_user_inputs


def main():

    data_dir = load_data_dir(project_dir)
    raw_data_dir = load_raw_data_dir(data_dir)

    candidate_list = get_user_inputs("clean", "files", raw_data_dir)
    print(f"User inputs list via data cleaning driver:\n{candidate_list}")
    caffeinate_process = start_caffeinate()
    try:
        for candidate in candidate_list:
            clean_one_candidate(candidate)
    finally:
        stop_caffeinate(caffeinate_process)


if __name__ == "__main__":
    main()