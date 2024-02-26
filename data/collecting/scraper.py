import os
import sys
from selenium import webdriver

from file_types.candidates import download_candidates
from file_types.committees import download_committees
from file_types.committee_contributions import download_committee_contributions
from file_types.individual_contributions import download_individual_contributions
from file_types.other_contributions import download_other_contributions
from firefox.firefox_driver import main as firefox_driver
from modules.await_downloads import await_downloads
from modules.get_year import get_year
from modules.load_page import load_page
from modules.move_files import move_files
from modules.unzip_files import unzip_files

collecting_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.dirname(collecting_dir)
sys.path.append(data_dir)
from directories import get_download_dir


def download_files(driver: webdriver.Firefox, input_year: str) -> tuple[bool, str | None]:
    success, election_year = download_candidates(driver, input_year)
    if not success:
        return False, None
    elif not download_committees(driver, election_year):
        return False, None
    elif not download_individual_contributions(driver, election_year):
        return False, None
    elif not download_committee_contributions(driver, election_year):
        return False, None
    elif not download_other_contributions(driver, election_year):
        return False, None
    return True, election_year


def manage_files(download_dir: str, election_year: str) -> None:
    if not await_downloads(download_dir):
        return
    elif not move_files(download_dir, election_year):
        return
    elif not unzip_files(election_year):
        return
    return


def main():
    input_year = get_year()
    download_dir = get_download_dir(input_year)
    driver_loaded, driver = firefox_driver(download_dir, True)
    if not driver_loaded:
        print("Failed to load web driver")
        return
    if not load_page(driver):
        return
    files_downloaded, election_year = download_files(driver, input_year)
    if not files_downloaded:
        driver.quit()
        return
    manage_files(download_dir, election_year)
    driver.quit()
    return


if __name__ == "__main__":
    main()
