import os
import sys

from engine import convert_one_candidate

current_dir = os.path.dirname(os.path.abspath(__file__))
converting_dir = os.path.dirname(current_dir)
data_dir = os.path.dirname(converting_dir)
sys.path.append(data_dir)
from caffeinate import start_caffeinate, stop_caffeinate
from data_directories import load_cleaned_files_dir
from user_inputs.driver_user_inputs import get_user_inputs


def main():

    caffeinate = start_caffeinate()

    try:

        input_files_dir = load_cleaned_files_dir()
        candidate_list = get_user_inputs("convert", "files", input_files_dir)
        print(f"\nCandidate list via data converting driver:\n{candidate_list}")
        candidate_count = len(candidate_list)
        purgatory_candidate_list = []

        for i, candidate in enumerate(candidate_list):
            success, purgatory_candidate = convert_one_candidate(candidate, i, candidate_count, False)
            if purgatory_candidate:
                purgatory_candidate_list.append(purgatory_candidate)
                print(f"\n{'~' * 100}\n{'~' * 100}\nCurrent purgatory list length: {len(purgatory_candidate_list)}\n{'~' * 100}\n{'~' * 100}\n")
                continue
            elif not success:
                print(f"\nFailed to convert data for {candidate}")
                continue

        purgatory_candidate_count = len(purgatory_candidate_list)
        if purgatory_candidate_count > 0:
            print(f"\n{'~' * 100}\n{'~' * 100}\nStarting to convert purgatory candidates\n")
            print(f"Purgatory candidates: {purgatory_candidate_list}")
            print(f"Purgatory candidate count: {purgatory_candidate_count}")
            for j, purgatory_candidate in enumerate(purgatory_candidate_list):
                success, _ = convert_one_candidate(purgatory_candidate, j, purgatory_candidate_count, True)

    except Exception as e:
        print(f"\nFailed to convert inputted data. Exception: {e}")

    finally:
        stop_caffeinate(caffeinate)


if __name__ == "__main__":
    main()
            