import os
import re
import shutil
import time
import zipfile
from pathlib import Path
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from firefox.firefox_driver import firefox_driver


def verify_dir_exists(dir: str):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok = True)


scraping_dir = Path(__file__).resolve().parent
data_dir = scraping_dir.parent
data_files_dir = os.path.join(data_dir, "data_files")
verify_dir_exists(data_files_dir)
raw_dir = os.path.join(data_files_dir, "raw")
verify_dir_exists(raw_dir)
headers_dir = os.path.join(data_files_dir, "headers")
verify_dir_exists(headers_dir)


def get_year() -> int:
    year = int(input("Year?\n> "))
    return year


def create_downloads_container(year: str) -> str:
    downloads_container_dir = os.path.join(data_files_dir, f"downloads_container_{year}")
    verify_dir_exists(downloads_container_dir)
    return downloads_container_dir


def load_driver(download_dir: str):
    driver_loaded, driver = firefox_driver(download_dir)
    if not driver_loaded:
        print("Failed to load web driver")
        driver.quit()
        return
    return driver


def load_page(driver) -> None:
    bulk_data_url = "https://www.fec.gov/data/browse-data/?tab=bulk-data"
    driver.get(bulk_data_url)
    return


def toggle_candidate_master_pane(driver) -> None:
    pane_locator = (By.CSS_SELECTOR, "#first-content-1")
    pane_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(pane_locator)
    )
    pane_status = pane_element.get_attribute("aria-hidden")
    if pane_status.lower() == "true":
        pane_button_locator = (
            By.CSS_SELECTOR,
            "button.js-accordion-trigger:nth-child(3)"
        )
        pane_button_element = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable(pane_button_locator)
        )
        pane_button_element.click()
    return


def find_input_year(driver, locator: str, input_year: int, find_year: bool) -> str | None:
    years_list_element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located(locator)
    )
    years_list_items = years_list_element.find_elements(By.TAG_NAME, "li")
    for years_list_item in years_list_items:
        years_link = years_list_item.find_element(By.TAG_NAME, "a")
        years_text = years_list_item.text
        years = re.findall(r"\d{4}", years_text)
        if years and int(years[0]) <= input_year <= int(years[1]):
            years_link.click()
            election_year = years[1]
            print("Downloaded file for", input_year)
            break
    if find_year:
        return election_year
    return


def download_candidate_master(driver, input_year: int) -> str:
    toggle_candidate_master_pane(driver)
    years_list_locator = (
        By.CSS_SELECTOR,
        "#first-content-1 > div:nth-child(3) > ul:nth-child(1)"
    )
    election_year = find_input_year(driver, years_list_locator, input_year, True)
    return election_year


def download_candidate_master_header(driver) -> None:
    toggle_candidate_master_pane(driver)
    header_button_locator = (
        By.CSS_SELECTOR,
        "p.icon-download--inline--left:nth-child(4) > a:nth-child(1)"
    )
    header_button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(header_button_locator)
    )
    header_button_element.click()
    print("Downloaded candidate master header")
    return


def download_individual_contributions(driver, input_year: int) -> None:
    button_locator = (
        By.CSS_SELECTOR,
        "button.js-accordion-trigger:nth-child(13)"
    )
    button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(button_locator)
    )
    button_element.click()
    years_list_locator = (
        By.CSS_SELECTOR,
        "#first-content-6 > div:nth-child(2) > ul:nth-child(1)"
    )
    find_input_year(driver, years_list_locator, input_year, False)
    print("Downloaded individual contributions file")
    return


def download_individual_contributions_header(driver) -> None:
    button_locator = (
        By.CSS_SELECTOR,
        "#first-content-6 > p:nth-child(3) > a:nth-child(1)"
    )
    button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(button_locator)
    )
    button_element.click()
    print("Downloaded indivudal contributions header")
    return


def download_committee_contributions(driver, input_year: int) -> None:
    button_locator = (
        By.CSS_SELECTOR,
        "button.js-accordion-trigger:nth-child(15)"
    )
    button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(button_locator)
    )
    button_element.click()
    years_list_locator = (
        By.CSS_SELECTOR,
        "#first-content-7 > div:nth-child(2) > ul:nth-child(1)"
    )
    find_input_year(driver, years_list_locator, input_year, False)
    print("Downloaded committee contributions file")
    return


def download_committee_contributions_header(driver) -> None:
    button_locator = (
        By.CSS_SELECTOR,
        "#first-content-7 > p:nth-child(3) > a:nth-child(1)"
    )
    button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(button_locator)
    )
    button_element.click()
    print("Downloaded committee contributions header")
    return


def download_other_contributions(driver, input_year: int):
    button_locator = (
        By.CSS_SELECTOR,
        "button.js-accordion-trigger:nth-child(17)"
    )
    button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(button_locator)
    )
    button_element.click()
    years_list_locator = (
        By.CSS_SELECTOR,
        "ul.u-margin--bottom"
    )
    find_input_year(driver, years_list_locator, input_year, False)
    print("Downloaded other contributions file")
    return


def download_other_contributions_header(driver):
    button_locator = (
        By.CSS_SELECTOR,
        "#first-content-8 > p:nth-child(3) > a:nth-child(1)"
    )
    button_element = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable(button_locator)
    )
    button_element.click()
    print("Downloaded other contributions header")
    return


def wait_for_downloads(src_dir):
    downloads_complete = False
    while not downloads_complete:
        downloads_complete = True
        for file_name in os.listdir(src_dir):
            if file_name.endswith(".part"):
                downloads_complete = False
                break
        if not downloads_complete:
            time.sleep(1)
    print("All files downloaded")
    return


def move_files(download_dir: str):
    wait_for_downloads(download_dir)
    for file_name in os.listdir(download_dir):
        if "header" in file_name.lower():
            header_src_path = os.path.join(download_dir, file_name)
            header_dst_path = os.path.join(headers_dir, file_name)
            shutil.move(header_src_path, header_dst_path)
            print("Finished moving", file_name)
        elif file_name.endswith(".zip"):
            year = file_name[-6:-4]
            if 80 <= int(year) <= 99:
                year_dir = os.path.join(raw_dir, "19" + year)
            else:
                year_dir = os.path.join(raw_dir, "20" + year)
            verify_dir_exists(year_dir)
            year_src_path = os.path.join(download_dir, file_name)
            year_dst_path = os.path.join(year_dir, file_name)
            shutil.move(year_src_path, year_dst_path)
            print("Finished moving", file_name)
    shutil.rmtree(download_dir)
    return



def unzip_year_files(year: str):
    year_dir = os.path.join(raw_dir, year)
    for src_file_name in os.listdir(year_dir):
        file_type = src_file_name[:-6]
        src_path = os.path.join(year_dir, src_file_name)
        dst_path = os.path.join(year_dir, file_type)
        if src_file_name.endswith(".zip"):
            with zipfile.ZipFile(src_path, "r") as z:
                z.extractall(dst_path)
                os.remove(src_path)
                print("Finished unzipping", src_file_name)
    return


def main():
    input_year = get_year()
    download_dir = create_downloads_container(str(input_year))
    driver = load_driver(download_dir)
    load_page(driver)
    election_year = download_candidate_master(driver, input_year)
    download_candidate_master_header(driver)
    download_individual_contributions(driver, input_year)
    download_individual_contributions_header(driver)
    download_committee_contributions(driver, input_year)
    download_committee_contributions_header(driver)
    download_other_contributions(driver, input_year)
    download_other_contributions_header(driver)
    move_files(download_dir)
    unzip_year_files(election_year)
    driver.quit()


if __name__ == "__main__":
    main()