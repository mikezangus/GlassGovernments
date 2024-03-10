import os
from utils.directories import get_raw_dir


def decide_year(from_files: bool) -> str:
    if from_files:
        year_dirs = os.listdir(get_raw_dir())
        year_options = [y for y in year_dirs if y.isdigit()]
        sorted_year_options = sorted(
            year_options,
            key = lambda x: int(x)
        )
        formatted_year_options = ', '.join(sorted_year_options)
    while True:
        if from_files:
            msg = f"\nFor which year do you want to process data?\nAvailable years: {formatted_year_options}\n> "
        else:
            msg = f"\nFor which year do you want to process data?\n> "
        year = input(msg)
        if not from_files:
            return year
        if year in year_options:
            return year
        print(f"\n{year} isn't an available year, try again")