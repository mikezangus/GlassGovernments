import os
import sys
from workflows_data_cleaning import determine_workflow

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from project_directories import user_inputs_dir, raw_data_dir, cleaned_data_dir
user_inputs_dir = os.path.join(project_dir, user_inputs_dir)
sys.path.append(user_inputs_dir)
from driver_user_inputs import main as get_user_inputs


def main():
    
    action = "clean"
    data_source = "files"
    year, chamber_list, state_list, district_list, candidate_list = get_user_inputs(data_source = data_source, action = action)
    determine_workflow(year, chamber_list, state_list, district_list, candidate_list, raw_data_dir, cleaned_data_dir)


if __name__ == "__main__":
    main()