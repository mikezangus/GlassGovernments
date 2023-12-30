import os
import sys
from workflows import determine_workflow

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import raw_data_dir, cleaned_data_dir
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    year_list, chamber_list, state_list, district_list, candidate_list = get_user_inputs("files", "clean")
    determine_workflow(year_list, chamber_list, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)


if __name__ == "__main__":
    main()