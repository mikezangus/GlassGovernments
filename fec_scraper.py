import logging, os, re, time
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait


DOWNLOADS_CONTAINER = os.path.abspath(os.path.join("data", "downloads_container"))

STATE_CODES = {
    # "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR", "california": "CA",
    # "colorado": "CO", "connecticut": "CT", "delaware": "DE", "florida": "FL", "georgia": "GA",
    # "hawaii": "HI", "idaho": "ID", "illinois": "IL", "indiana": "IN", "iowa": "IA",
    # "kansas": "KS", "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    # "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO",
    "montana": "MT", "nebraska": "NE", "nevada": "NV", "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM",
    "new york": "NY", "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT", "vermont": "VT",
    "virginia": "VA", "washington": "WA", "west virginia": "WV", "wisconsin": "WI", "wyoming": "WY"
}
AT_LARGE_STATES = ["AK", "DE", "ND", "SD", "VT", "WY"]
#MT,


def firefox_driver():
    options = Options()
    options.headless = False
    firefox_preferences = {
        "browser.privatebrowsing.autostart": True,
        "browser.cache.disk.enable": False,
        "browser.cache.memory.enable": False,
        "browser.cache.offline.enable": False,
        "network.http.use-cache": False,
        "layout.css.devPixelsPerPx": "1",
        "browser.download.dir": DOWNLOADS_CONTAINER,
        "browser.download.folderList": 2,
        "browser.download.useDownloadDir": True,
    }
    for preference, value in firefox_preferences.items():
        options.set_preference(preference, value)
     
    profile = webdriver.FirefoxProfile(os.path.join("scraper_support", "firefox_profile_selenium"))
    driver = webdriver.Firefox(
        executable_path = os.path.join("scraper_support", "geckodriver"), service_log_path = os.path.join("scraper_support", "geckodriver.log"), options = options, firefox_profile = profile)
    driver.maximize_window()
    return driver


class DataSelector:
    def __init__(self):
        self.body = None
        self.state = None
        self.district = None
    def select_body(self):
        while True:
            body = input("House or Senate?: ").lower().strip()
            if body in ["house", "senate"]:
                self.body = body
                break
            else:
                print("Invalid, choose either House or Senate")
    @staticmethod
    def is_valid_state(state):
        return state.upper() in STATE_CODES.values() or state.lower() in STATE_CODES
    def select_state(self):
        while True:
            state_amount = input(f"Download {self.body} data for all states (y/n)?: ").lower()
            if state_amount == "y":
                self.state = "all"
                break
            elif state_amount == "n":
                state = input("Which state?: ").strip()
                if self.is_valid_state(state):
                    if state.lower() in STATE_CODES:
                        state = STATE_CODES[state.lower()]
                    self.state = state.upper()
                    break
                else:
                    print("Invalid state")
            else:
                print("Invalid state amount")
    def select_district(self):
        if self.body == "house" and self.state != "all" and self.state not in AT_LARGE_STATES:
            while True:
                district_amount = input(f"Download data for all {self.state} districts (y/n)?: ").lower()
                if district_amount == "y":
                    self.district = "all"
                    break
                elif district_amount == "n":
                    self.district = input("Which district?: ")
                    break
                else:
                    print("Invalid")
        else:
            self.district = "all" if self.state == "all" else "00"
    def data_selections(self):
        self.select_body()
        self.select_state()
        self.select_district()
        return self.body, self.state, self.district


class FileManager:
    @staticmethod
    def prepare_downloads_container(indent):
        if not os.path.exists(DOWNLOADS_CONTAINER):
            os.makedirs(DOWNLOADS_CONTAINER)
            print(indent + f"downloads_container created at directory {DOWNLOADS_CONTAINER}")
        for filename in os.listdir(DOWNLOADS_CONTAINER):
            file_path = os.path.join(DOWNLOADS_CONTAINER, filename)
            if os.path.isfile(file_path):
                os.unlink(file_path)
                print(f"{indent}Successfully cleared {file_path}")
    @staticmethod
    def download_file(year, state, district, last_name, first_name, party, indent):
        if not os.listdir(DOWNLOADS_CONTAINER):
            print(indent + f"No file found in downloads container")
            logging.info(f"Download failed for candidate: {first_name} {last_name} ({party}), State: {state}, District: {str(district).zfill(2)}")
            return
        for downloaded_file in os.listdir(DOWNLOADS_CONTAINER):
            src_path = os.path.join(DOWNLOADS_CONTAINER, downloaded_file)
            if os.path.isfile(src_path):
                dst_path = os.path.join("data", year, state, district)
                os.makedirs(dst_path, exist_ok = True)
                file_name = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_source.csv"
                dst_path = os.path.join(dst_path, file_name)
                os.rename(src_path, dst_path)
                print(indent + f"File created at directory: {dst_path}")


class Scraper:
    def __init__(self, state, district, year):
        self.state = state
        self.district = district
        self.year = year
    @staticmethod
    def load_page(driver, indent, timeout = 60, retries = 10, delay = 10):
        for attempt in range(1, retries + 1):
            try:
                WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return jQuery.active==0"))
                WebDriverWait(driver, timeout).until(lambda d: d.execute_script("return document.readyState") == "complete")
                return True
            except Exception as e:
                print(indent + f"Failed to load page on attempt {attempt}/{retries} due to error: {e}")
                if attempt < retries:
                    time.sleep(delay)
                    print(indent + f"Retrying for attempt {attempt}/{retries} for maximum of {timeout} seconds")
                else:
                    exit_message = indent + f"Reached maximium retry attempts, exiting"
                    print(exit_message)
                    logging.error(exit_message)
                    return None
    def prepare_for_scrape(self, district):
        if self.state.upper() in AT_LARGE_STATES:
            district = "00"
        house_url = f"https://www.fec.gov/data/elections/house/{self.state}/{str(district).zfill(2)}/{self.year}/"
        max_attempts = 25
        for attempt in range(max_attempts):
            try:
                driver.get(house_url)
                self.load_page(driver, indent = "")
                break
            except Exception as e:
                print(f"Failed to load district's page. Exception: {e}. Retrying for attempt {attempt}/{max_attempts}")
                time.sleep(10)
                if attempt + 1 >= max_attempts:
                    print(f"Failed to load district's page after {max_attempts} attempts")
                    return

    def download_candidate(self, i, candidate_count, district):

        # Setup
        current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_path = os.path.join("scraper_support", "logs")
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        log_filename = f"{log_path}/failed_downloads_{current_date_time}.log"
        logging.basicConfig(filename = log_filename, level = logging.INFO, format = "%(asctime)s - %(levelname)s - %(message)s")
        indent_length = len(f"{self.state}-{str(district).zfill(2)} {i + 1}/{candidate_count}: ")
        indent = " " * indent_length
        max_attempts = 5

        # Find candidate
        for attempt in range(max_attempts):
            self.load_page(driver, indent)
            candidate_css_base = f"#DataTables_Table_0 > tbody:nth-child(2) > tr:nth-child({i + 1})"
            selectors = [" > td:nth-child(1)", " > td:nth-child(2)", " > td:nth-child(3)"]
            data_elements = []
            for selector in selectors:
                try:
                    locator = (By.CSS_SELECTOR, candidate_css_base + selector)
                    element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(locator))
                    data_elements.append(element.text)
                except Exception as e:
                    print(indent + f"Exception: {e}\nAttempt {attempt + 1}/{max_attempts}. Retrying...")
                    break
            else:
                full_name_element, party_element, total_receipts_element = data_elements
                full_name = full_name_element.split(", ")
                last_name, first_name = full_name[0].rstrip(",").replace(" ", "-"), full_name[1].replace(" ", "-")
                total_receipts = float(re.sub("[,$]", "", total_receipts_element))
                if total_receipts == 0:
                    print(f"{self.state}-{str(district).zfill(2)} {i + 1}/{candidate_count}: {first_name} {last_name} received ${total_receipts:.2f} in donations, skipping")
                    return
                else:
                    party = party_element.split(" ")[0] if party_element else "NO-PARTY-FOUND"
                    print(f"{self.state}-{str(district).zfill(2)} {i + 1}/{candidate_count}: Scraping for {first_name} {last_name} ({party}), who received ${total_receipts:,.2f} in donations")
                    candidate_locator = (By.CSS_SELECTOR, candidate_css_base + "> td:nth-child(1) > a:nth-child(1)")
                    candidate_element = WebDriverWait(driver, 15).until(EC.presence_of_element_located(candidate_locator))
                    candidate_element.click()
                break
        else:
            print(indent + f"Failed after {max_attempts} attempts. Moving to next candidate")
            logging.info(f"Failed to find candidate. State: {self.state}, District: {str(district).zfill(2)}")

        # Check if candidate has funding data
        for attempt in range(max_attempts):
            self.load_page(driver, indent)
            try:
                funding_element = (By.CSS_SELECTOR, "div.entity__figure--narrow:nth-child(4) > div:nth-child(1)")
                funding_text = WebDriverWait(driver, 60).until(EC.presence_of_element_located(funding_element)).text
                if f"We don't have" in funding_text:
                    print(indent + f"Attempt {attempt + 1}: No funding data found for {first_name} {last_name}. Retrying...")
                    if attempt < max_attempts - 1:
                        driver.refresh()
                        time.sleep(5)
                    else:
                        print(f"{indent}No funding data for {first_name} {last_name}, skipping")
                        driver.back()
                        return
                else:
                    break
            except Exception as e:
                print(indent + f"Exception: {e}\nAttempt {attempt + 1}/{max_attempts} to check for funding data. Retrying...")
                if attempt < max_attempts - 1:
                    driver.refresh()
                    time.sleep(5)
                else:
                    error_message = indent + f"Exception: {e}\n Failed after {max_attempts} attempts. Moving to next candidate"
                    print(error_message)
                    logging.info(f"Check for funding data failed for candidate: {first_name} {last_name}, State: {self.state}, District: {str(district).zfill(2)}")
                    return

        # Browse receipts
        for attempt in range(max_attempts):
            self.load_page(driver, indent)
            try:
                browse_receipts_element = (By.CSS_SELECTOR, "#total-raised > div:nth-child(1) > a:nth-child(2)")
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable(browse_receipts_element)).click()
                break
            except Exception as e:
                print(indent + f"Exception: {e}.\nAttempt {attempt + 1}/{max_attempts} to click on browse receipts. Retrying...")
                if attempt < max_attempts - 1:
                    driver.refresh()
                    time.sleep(5)
                else:
                    error_message = indent + f"Exception: {e}\n Failed after {max_attempts} attempts. Moving to next candidate"
                    print(error_message)
                    logging.info(f"Download failed for candidate: {first_name} {last_name}, State: {self.state}, District: {str(district).zfill(2)}")
                    return
        
        # Check if export available
        for attempt in range(max_attempts):
            self.load_page(driver, indent)
            try:
                self.load_page(driver, indent)
                data_container_element = (By.CSS_SELECTOR, ".data-container__action")
                WebDriverWait(driver, 30).until(EC.visibility_of_element_located(data_container_element))
                export_locator = (By.CSS_SELECTOR, ".js-export.button.button--cta.button--export")
                export_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located(export_locator))
                if "is-disabled" not in export_element.get_attribute("class"):
                    break
                time.sleep(5)  
            except Exception as e:
                print(indent + f"Exception: {e}.\nAttempt {attempt + 1}/{max_attempts} to click on browse receipts. Retrying...")
                driver.refresh()
                time.sleep(5)
                if attempt >= max_attempts - 1:
                    print(indent + f"Exception: {e}\n Failed to check export availability for {first_name} {last_name}. Moving to next candidate")
                    logging.info(f"Download failed for candidate: {first_name} {last_name}, State: {self.state}, District: {str(district).zfill(2)}")
                    return
        if "is-disabled" in export_element.get_attribute("class"):
            print(indent + f"{first_name} {last_name}'s export button is disabled, skipping")
            logging.info(f"Export button disabled for candidate: {first_name} {last_name}, State: {self.state}, District: {str(district).zfill(2)}")
            time.sleep(1)
            driver.back()
            time.sleep(1)
            driver.back()
            return
        elif "This table has no data to export." in driver.page_source:
            print(indent + f"{first_name} {last_name} has no data to export, skipping")
            logging.info(f"No data to export for candidate: {first_name} {last_name}, State: {self.state}, District: {str(district).zfill(2)}")
            time.sleep(1)
            driver.back()
            time.sleep(1)
            driver.back()
            return

        # Export and download
        FileManager.prepare_downloads_container(indent)
        download_attempts = 0
        max_download_attempts = 20
        for download_attempt in range(max_download_attempts):
            start_time = time.time()
            try:
                self.load_page(driver, indent)
                export_element.click()
                downloads_pane_element = (By.CSS_SELECTOR, ".downloads")
                WebDriverWait(driver, 30).until(EC.presence_of_element_located(downloads_pane_element))
                preparing_download_text = "We're preparing your download"
                WebDriverWait(driver, 120).until_not(EC.text_to_be_present_in_element(downloads_pane_element, preparing_download_text))
                download_element = (By.CSS_SELECTOR, "a.button")
                WebDriverWait(driver, 30).until(EC.element_to_be_clickable(download_element)).click()
                success_end_time = time.time()
                print(indent + f"Download attempt {download_attempts + 1}: Successfully started downloading {first_name} {last_name}'s data in {round(success_end_time - start_time, 1)} seconds")
                break
            except Exception as e:
                downloads_pane_text = WebDriverWait(driver, 30).until(EC.presence_of_element_located(downloads_pane_element)).text.lower()
                if "exceeded your maximum downloads" in downloads_pane_text:
                    print(indent + "Maximum hourly download limit met")
                    for _ in range(10):
                        for minute in range(30, 0, -1):
                            print(indent + f"Retrying in {minute} minute(s)")
                            time.sleep(60)
                        try:
                            self.load_page(driver, indent)
                            export_element.click()
                            downloads_pane_element = (By.CSS_SELECTOR, ".downloads")
                            WebDriverWait(driver, 30).until(EC.presence_of_element_located(downloads_pane_element))
                            preparing_download_text = "We're preparing your download"
                            WebDriverWait(driver, 120).until_not(EC.text_to_be_present_in_element(downloads_pane_element, preparing_download_text))
                            download_element = (By.CSS_SELECTOR, "a.button")
                            WebDriverWait(driver, 30).until(EC.element_to_be_clickable(download_element)).click()
                            success_end_time = time.time()
                            print(indent + f"Download attempt {download_attempts + 1}: Successfully started downloading {first_name} {last_name}'s data in {round(success_end_time - start_time, 1)} seconds")
                            break
                        except Exception as ee:
                            print(indent + f"Still unable to download. Error: {ee}")
                            continue
                print(indent + f"Exception: {e}")
                print(indent + f"Download attempt {download_attempt + 1}/{max_download_attempts}. Retrying...")
                if download_attempt >= max_download_attempts - 1:
                    print(indent + f"Failed to download {first_name} {last_name}'s data, moving to the next candidate")
                    logging.info(f"Download failed for candidate: {first_name} {last_name}, State: {self.state}, District: {str(district).zfill(2)}")
                    break
            time.sleep(5)
        try:
            FileManager.download_file(year, self.state, str(district).zfill(2), last_name, first_name, party, indent)
            close_download_element = (By.CSS_SELECTOR, "button.js-close:nth-child(3)")
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable(close_download_element)).click()
        except Exception as e:
            print(e)

    def download_all_candidates_in_district(self, district):
        if not self.check_if_district_exists():
            print(f"District {district} does not exist for state {self.state}. Moving to the next district.")
            return
        try:
            candidate_count_locator = (By.CSS_SELECTOR, "#DataTables_Table_0_info")
            candidate_count_element = WebDriverWait(driver, 60).until(lambda d: d.find_element(*candidate_count_locator) if EC.text_to_be_present_in_element(candidate_count_locator, "Showing")(d) else False)
            candidate_count = int(candidate_count_element.text.split(" ")[-2])
        except TimeoutException:
            print(f"No candidate count element found for district {district} in state {self.state}. Moving to the next district/state.")
            return
        print(f"\n{self.state} DISTRICT {str(district).zfill(2)} {'—' * 100}")
        for i in range(candidate_count):
            if i > 9:
                success = False
                while not success:
                    try:
                        results_per_page_locator = (By.CSS_SELECTOR, "#DataTables_Table_0_length > label:nth-child(1) > select:nth-child(1)")
                        results_per_page_element = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(results_per_page_locator))
                        time.sleep(1)
                        Select(results_per_page_element).select_by_value("100")
                        success = True
                    except Exception:
                        driver.refresh()
                        time.sleep(10)
            self.download_candidate(i, candidate_count, district)
            self.prepare_for_scrape(district)

    def download_one_district(self):
        self.prepare_for_scrape(self.district)
        self.download_all_candidates_in_district(self.district)

    def check_if_district_exists(self):
        try:
            if not self.load_page(driver, indent = ""):
                logging.error(f"Failed to load page for {self.state}-{str(district).zfill(2)}")
                return False
            financial_totals_locator = (By.CSS_SELECTOR, "#candidate-financial-totals > div:nth-child(2)")
            financial_totals_element = WebDriverWait(driver, 60).until(EC.presence_of_element_located(financial_totals_locator)).text
            if "We don't have" in financial_totals_element:
                return False
            return True
        except TimeoutException as e:
            print(f"TimeoutException: {e}")
            print(driver.page_source)
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False

    def download_all_districts(self):
        if self.state.upper() in AT_LARGE_STATES:
            self.district = "00"
            self.prepare_for_scrape(self.district)
            self.download_all_candidates_in_district(self.district)  
        else:
            for district in range(1, 100):
                self.prepare_for_scrape(district)
                if not self.check_if_district_exists():
                    print(f"{self.state} has {district - 1} districts")
                    break
                self.download_all_candidates_in_district(district)

    def download_all_states(self):
        for state_code in STATE_CODES.values():
            print(f"\n\n{'—' * 125}\nSTARTING SCRAPING FOR {state_code} {'—' * 100}\n{'—' * 125}")
            self.state = state_code.upper()
            self.download_all_districts()


if __name__ == "__main__":

    selections = DataSelector()
    year = "2022"
    body, state, district = selections.data_selections()

    driver = firefox_driver()
    scraper = Scraper(state, district, year)
    if state == "all":
        scraper.download_all_states()
    elif district == "all":
        scraper.download_all_districts()
    else:
        scraper.download_one_district()



