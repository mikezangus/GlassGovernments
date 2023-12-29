import sys
import os
from workflows_data_collection import determine_workflow
from modules.log_creator import create_log_file

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import user_inputs_dir
sys.path.append(user_inputs_dir)
from driver_user_inputs import main as get_user_inputs


def main():
    data_source = "internet"
    action = "scrape"
    year, chamber, state, district = get_user_inputs(data_source = data_source, action = action)
    create_log_file()
    determine_workflow(year = year, chamber = chamber, state = state, district = district)


if __name__ == "__main__":
    main()