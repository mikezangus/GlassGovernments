import os
import subprocess
import sys
from engine import clean_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
driver_path = os.path.join(current_dir, "driver.py")
print(f"Driver file path: {driver_path}")
shell_file_path = os.path.join(current_dir, "modules", "terminal_opener.sh")
print(f"Shell file path: {shell_file_path}")
project_dir = os.path.dirname(current_dir)
sys.path.append(project_dir)
from caffeinate import start_caffeinate, stop_caffeinate
from project_directories import load_data_dir, load_raw_data_dir
from user_inputs.driver_user_inputs import get_user_inputs


def main():
    caffeinate = start_caffeinate()
    try:
        data_dir = load_data_dir(project_dir)
        raw_data_dir = load_raw_data_dir(data_dir)
        candidate_list = get_user_inputs("clean", "files", raw_data_dir)
        candidate_count = len(candidate_list)
        purgatory_list = []
        print(f"\nCandidate list via data cleaning driver:\n{candidate_list}")
        print(f"\nStarted to clean data for {candidate_count:,} candidates\n")
        for i, candidate in enumerate(candidate_list):
            _, purgatory_candidate = clean_one_candidate(candidate, i, candidate_count, False)
            if purgatory_candidate:
                purgatory_list.append(purgatory_candidate)
                print(f"\n{'~' * 100}\n{'~' * 100}\nCurrent purgatory list:\n{purgatory_list}\n{'~' * 100}\n{'~' * 100}\n")
        purgatory_count = len(purgatory_list)
        if purgatory_count > 0:
            print(f"\nStarting to process {purgatory_count} purgatory candidates\n")
            for i, purgatory_candidate in enumerate(purgatory_list):
                _, _ = clean_one_candidate(purgatory_candidate, i, purgatory_count, True)
    except Exception as e:
        print(f"\nFailed to clean inputted data. Exception: {e}")
    finally:
        stop_caffeinate(caffeinate)
        print(f"\nFinished cleaning inputted data")
        print(f"\nExiting data cleaning driver\n")


if __name__ == "__main__":
    main()