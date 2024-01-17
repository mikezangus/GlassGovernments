import os
import subprocess
import sys

from engine import convert_one_candidate
from modules.purgatory_manager import extract_purgatory_list

converting_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(converting_dir)
caffeinate_path = os.path.join(data_dir, "caffeinate.sh")
sys.path.append(data_dir)
from data_directories import load_cleaned_files_dir
from user_inputs.driver_user_inputs import get_user_inputs


def main():

    subprocess.run([caffeinate_path, "start"])

    try:

        input_files_dir = load_cleaned_files_dir()
        candidate_list = get_user_inputs("convert", "files", input_files_dir)
        print(f"\nCandidate list via data converting driver:\n{candidate_list}")
        candidate_count = len(candidate_list)
        purgatory_constituency_set = set()

        for i, candidate in enumerate(candidate_list):
            split_index = [pos for pos, char in enumerate(candidate) if char == "_"][3]
            constituency = candidate[:split_index]
            success, purgatory = convert_one_candidate(candidate, i, candidate_count, False, constituency)
            if purgatory:
                purgatory_constituency_set.add(constituency)
                continue
            if not success:
                print(f"\nFailed to convert data for {candidate}")
                continue

        for constituency in purgatory_constituency_set:
            purgatory_list = extract_purgatory_list(constituency)
            print(f"\nPurgatory list via data converting driver:\n{purgatory_list}")
            purgatory_count = len(purgatory_list)
            for i, purgatory_candidate in enumerate(purgatory_list):
                if not convert_one_candidate(purgatory_candidate, i, purgatory_count, True, constituency):
                    print(f"\nFailed to convert data for purgatory candidate {purgatory_candidate}")
                    continue

    except Exception as e:
        print(f"\nFailed to convert inputted data. Exception: {e}")

    finally:
        subprocess.run([caffeinate_path, "stop"])


if __name__ == "__main__":
    main()