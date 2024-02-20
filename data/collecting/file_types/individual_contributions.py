from selenium import webdriver
from .utilities import open_pane, download_main_file, download_header_file


def download_individual_contributions(driver: webdriver.Firefox, election_year: str) -> bool:
    subject = "Individual Contributions"
    try:
        open_pane(driver, "13")
        download_main_file(subject, "6", driver, election_year)
        download_header_file(subject, "6", driver)
        return True
    except Exception as e:
        print(subject, "| Error:", e)
        return False
