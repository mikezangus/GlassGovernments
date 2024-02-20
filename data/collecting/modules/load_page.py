from selenium import webdriver


def load_page(driver: webdriver.Firefox) -> bool:
    try:
        bulk_data_url = "https://www.fec.gov/data/browse-data/?tab=bulk-data"
        driver.get(bulk_data_url)
        return True
    except Exception as e:
        print("Load Page | Error:", e)
        return False
