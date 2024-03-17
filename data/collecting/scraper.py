import os
import sys
from utils.load_page import load_page
from utils.manage_files import manage_files

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(DATA_DIR)
from utils.decide_year import decide_year
from utils.directories import get_download_dir
from utils.download_files import download_files
from utils.firefox.load_webdriver import load_webdriver


def scraper():
    year = decide_year(False)
    download_dir = get_download_dir(year)
    driver_loaded, driver = load_webdriver(
        True,
        download_dir
    )
    if not driver_loaded:
        print("Failed to load web driver")
        return
    if not load_page(driver):
        return
    files_downloaded, election_year = download_files(
        driver,
        year
    )
    if not files_downloaded:
        driver.quit()
        return
    manage_files(
        download_dir,
        election_year
    )
    driver.quit()
    return


if __name__ == "__main__":
    scraper()
