import os
import sys

from engine import upload_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from user_inputs.driver_user_inputs import get_user_inputs
from project_directories import load_data_dir, load_cleaned_data_dir


def main():

    data_dir = load_data_dir(project_dir)
    cleaned_data_dir = load_cleaned_data_dir(data_dir)

    candidate_list = get_user_inputs("upload", "files", cleaned_data_dir)
    print(f"User inputs list via data uploading driver:\n{candidate_list}")
    for candidate in candidate_list:
        upload_one_candidate(candidate, cleaned_data_dir)


if __name__ == "__main__":
    main()