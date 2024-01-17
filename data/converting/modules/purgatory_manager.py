import os
import sys

modules_dir = os.path.dirname(os.path.abspath(__file__))
converting_dir = os.path.dirname(modules_dir)
data_dir = os.path.dirname(converting_dir)
sys.path.append(data_dir)
from data_directories import load_purgatory_list_dir


def load_purgatory_file(constituency: str):
    purgatory_dir = load_purgatory_list_dir()
    purgatory_file_name = f"purgatory_{constituency}.txt"
    purgatory_path = os.path.join(purgatory_dir, purgatory_file_name)
    return purgatory_path


def populate_purgatory_file(constituency: str, candidate: str):
    try:
        file_path = load_purgatory_file(constituency)
        if not os.path.exists(file_path):
            open(file_path, "w").close()
        with open(file_path, "r+") as file:
            lines = [line.strip() for line in file.readlines()]
            if candidate not in lines:
                file.write(candidate + "\n")
                return True
            else:
                return False
    except Exception as e:
        print(f"Error populating purgatory file: {e}")
        return False


def extract_purgatory_list(constituency: str):
    file_path = load_purgatory_file(constituency)
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]