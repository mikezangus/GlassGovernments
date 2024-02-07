import os
import sys
from pathlib import Path

modules_dir = Path(__file__).resolve().parent
processing_dir = Path(modules_dir.parent)
data_dir = str(processing_dir.parent)
sys.path.append(data_dir)
from directories import get_raw_dir


def decide_year() -> str:
    year_dirs = os.listdir(get_raw_dir())
    year_options = [y for y in year_dirs if y.isdigit()]
    sorted_year_options = sorted(
        year_options,
        key = lambda x: int(x)
    )
    formatted_year_options = ', '.join(sorted_year_options)
    while True:
        year = input(f"\nFor which year do you want to process raw data?\nAvailable years: {formatted_year_options}\n> ")
        if year in year_options:
            return year
        print(f"\n{year} isn't an available year, try again")
