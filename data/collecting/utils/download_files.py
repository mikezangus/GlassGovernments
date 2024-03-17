import os
import sys
from selenium import webdriver

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
COLLECTING_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(COLLECTING_DIR)
from file_types.candidates import download_candidates
from file_types.committees import download_committees
from file_types.individual_contributions import download_individual_contributions
from file_types.committee_contributions import download_committee_contributions
from file_types.other_contributions import download_other_contributions


def download_files(
    driver: webdriver.Firefox,
    input_year: str
) -> tuple[bool, str | None]:
    success, election_year = download_candidates(
        driver,
        input_year
    )
    if not success:
        return False, None
    elif not download_committees(
        driver,
        election_year
    ):
        return False, None
    elif not download_individual_contributions(
        driver,
        election_year
    ):
        return False, None
    elif not download_committee_contributions(
        driver,
        election_year
    ):
        return False, None
    elif not download_other_contributions(
        driver,
        election_year
    ):
        return False, None
    return True, election_year
