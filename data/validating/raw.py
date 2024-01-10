import os
import sys

validating_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(validating_dir)
sys.path.append(data_dir)
from data_directories import load_raw_files_dir


def check_file(file_path: str, file_name: str):
    if os.stat(file_path).st_size == 0:
        return file_name


raw_files_dir = load_raw_files_dir()

naughty_list = []

for year in os.listdir(raw_files_dir):
    year_dir = os.path.join(raw_files_dir, year)
    if os.path.isdir(year_dir):

        for chamber in os.listdir(year_dir):
            chamber_dir = os.path.join(year_dir, chamber)
            if os.path.isdir(chamber_dir):

                for state in os.listdir(chamber_dir):
                    state_dir = os.path.join(chamber_dir, state)
                    if os.path.isdir(state_dir):

                        if chamber.lower() == "house":
                            for district in os.listdir(state_dir):
                                district_dir = os.path.join(state_dir, district)
                                if os.path.isdir(district_dir):

                                    for file_name in os.listdir(district_dir):
                                        file_path = os.path.join(district_dir, file_name)
                                        empty_file = check_file(file_path, file_name)
                                        if empty_file:
                                            naughty_list.append(empty_file)
                        
                        elif chamber.lower() == "senate":
                            for file_name in os.listdir(state_dir):
                                file_path = os.path.join(state_dir, file_name)
                                empty_file = check_file(file_path, file_name)
                                if empty_file:
                                    naughty_list.append(empty_file)

                        else:
                            print("Error with chamber logic")
                        
print(naughty_list)
print(len(naughty_list))