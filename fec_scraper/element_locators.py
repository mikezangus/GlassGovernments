from selenium.webdriver.common.by import By


locator_funding = (By.CSS_SELECTOR, "div.entity__figure--narrow:nth-child(4) > div:nth-child(1)")
locator_browse_receipts = (By.CSS_SELECTOR, "#total-raised > div:nth-child(1) > a:nth-child(2)")
locator_data_container = (By.CSS_SELECTOR, ".data-container__action")
locator_export_button = (By.CSS_SELECTOR, ".js-export.button.button--cta.button--export")
locator_downloads_pane = (By.CSS_SELECTOR, ".downloads")
locator_download_button = (By.CSS_SELECTOR, "a.button")
locator_close_download_button = (By.CSS_SELECTOR, "button.js-close:nth-child(3)")