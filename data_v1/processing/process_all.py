import os
import sys
from candidates.process_candidates import process_candidates
from candidates.process_names import process_names
from committees.process_committees import process_committees
from contributions.process_contributions import process_all_contributions as process_contributions

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year


def process_all():
    year = decide_year(True)
    process_candidates(year)
    process_committees(year)
    process_contributions(year)
    process_names(year)
    return


if __name__ == "__main__":
    process_all()
