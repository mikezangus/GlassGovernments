import os
import sys

from workflows import determine_workflow

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    year, chamber_list, state_list, district_list, candidate_list = get_user_inputs("files", "upload")
    determine_workflow(year, chamber_list, state_list, district_list, candidate_list)


if __name__ == "__main__":
    main()