import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
CONTRIBUTIONS_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(CONTRIBUTIONS_DIR)
from process_contributions import process_contributions


def process_committees(year: str = None) -> None:
    process_contributions("Committee", "pas2", "itpas2.txt", year)
    return


if __name__ == "__main__":
    process_committees()
