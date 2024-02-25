import os
import sys

file_types_dir = os.path.dirname(os.path.abspath(__file__))
processing_dir = os.path.dirname(file_types_dir)
sys.path.append(processing_dir)
from process_contributions import process_contributions


def process_other_conts(year: str = None) -> None:
    process_contributions("Other", "oth", "itoth.txt", year)  
    return


if __name__ == "__main__":
    process_other_conts()
