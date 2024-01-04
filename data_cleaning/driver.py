import os
import sys
from engine import clean_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from user_inputs.driver_user_inputs import get_user_inputs
from project_directories import load_data_dir, load_raw_data_dir


def main():

    data_dir = load_data_dir(project_dir)
    raw_data_dir = load_raw_data_dir(data_dir)

    candidate_list = get_user_inputs("clean", "files", raw_data_dir)
    for candidate in candidate_list:
        clean_one_candidate(candidate)


if __name__ == "__main__":
    main()