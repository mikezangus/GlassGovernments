from selenium import webdriver
from .utilities import open_pane, download_main_file, download_header_file


def download_committees(driver: webdriver.Firefox, election_year: str) -> bool:
    subject = "Committees"
    try:
        open_pane(driver, "5")
        download_main_file(subject, "2", driver, election_year)
        download_header_file(subject, "2", driver)
        return True
    except Exception as e:
        print(subject, "| Error:", e)
        return False
