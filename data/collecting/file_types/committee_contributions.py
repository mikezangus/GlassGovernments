from selenium import webdriver
from .utilities import open_pane, download_main_file, download_header_file


def download_committee_contributions(driver: webdriver.Firefox, election_year: str) -> bool:
    subject = "Committee Contributions"
    try:
        open_pane(driver, "15")
        download_main_file(subject, "7", driver, election_year)
        download_header_file(subject, "7", driver)
        return True
    except Exception as e:
        print(subject, "| Error:", e)
        return False
