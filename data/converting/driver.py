import os
import sys

from engine import convert_one_candidate
from modules.purgatory_list_populator import extract_purgatory_list

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
        purgatory_status = False

        for i, candidate in enumerate(candidate_list):
            success, purgatory = convert_one_candidate(candidate, i, candidate_count, False)
            if purgatory:
                purgatory_status = True
                continue
            if not success:
                print(f"\nFailed to convert data for {candidate}")
                continue
        
        if purgatory_status:
            purgatory_list = extract_purgatory_list()
            print(f"\nPurgatory list via data converting driver:\n{purgatory_list}")
            purgatory_count = len(purgatory_list)
            for i, purgatory_candidate in enumerate(purgatory_list):
                if not convert_one_candidate(purgatory_candidate, i, purgatory_count, True):
                    print(f"\nFailed to convert data for purgatory candidate {purgatory_candidate}")
                    continue

    except Exception as e:
        print(f"\nFailed to convert inputted data. Exception: {e}")

    finally:
        stop_caffeinate(caffeinate)


if __name__ == "__main__":
    main()
            