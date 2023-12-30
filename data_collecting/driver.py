import sys
import os
from workflows import determine_workflow
from modules.sub_modules.log_creator import create_log_file

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    data_source = "internet"
    action = "scrape"
    year, chamber_list, state_list, district_list = get_user_inputs(data_source, action)
    create_log_file()
    determine_workflow(year, chamber_list, state_list, district_list)


if __name__ == "__main__":
    main()