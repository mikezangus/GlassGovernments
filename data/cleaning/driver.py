import os
import sys
from engine import clean_one_candidate

cleaning_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(cleaning_dir)
sys.path.append(data_dir)
from data_directories import load_raw_files_dir
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    try:
        input_files_dir = load_raw_files_dir()
        candidate_list = get_user_inputs("clean", "files", input_files_dir)
        candidate_count = len(candidate_list)
        for i, candidate in enumerate(candidate_list):
           if not clean_one_candidate(candidate, i, candidate_count):
               continue
    except Exception as e:
        print(f"\nFailed to clean inputted data. Exception: {e}")
    finally:
        print(f"\nFinished cleaning inputted data")
        print(f"\nExiting data cleaning driver\n")


if __name__ == "__main__":
    main()