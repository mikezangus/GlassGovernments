import os
import sys


modules_dir = os.path.dirname(os.path.abspath(__file__))
converting_dir = os.path.dirname(modules_dir)
data_dir = os.path.dirname(converting_dir)
sys.path.append(data_dir)
from data_directories import load_purgatory_list_dir


def load_purgatory_file():
    purgatory_dir = load_purgatory_list_dir()
    purgatory_file_name = f"purgatory.txt"
    purgatory_path = os.path.join(purgatory_dir, purgatory_file_name)
    return purgatory_path


def populate_purgatory_file(candidate: str):
    try:
        file_path = load_purgatory_file()
        with open(file_path, "a") as file:
            file.write(candidate + "\n")
        return True
    except:
        return False


def extract_purgatory_list():
    file_path = load_purgatory_file()
    with open(file_path, 'r') as file:
        return [line.strip() for line in file.readlines()]