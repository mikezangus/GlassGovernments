from selenium.webdriver.common.by import By


locator_funding = (By.CSS_SELECTOR, "div.entity__figure--narrow:nth-child(4) > div:nth-child(1)")
locator_browse_receipts_button = (By.CSS_SELECTOR, "#total-raised > div:nth-child(1) > a:nth-child(2)")
locator_data_container = (By.CSS_SELECTOR, ".data-container__action")
locator_donation_count = (By.CSS_SELECTOR, ".tags__count")
locator_export_button = (By.CSS_SELECTOR, ".js-export.button.button--cta.button--export")
locator_export_message = (By.CSS_SELECTOR, ".js-export-message")
locator_downloads_pane = (By.CSS_SELECTOR, ".downloads")
locator_download_button = (By.CSS_SELECTOR, "a.button")
locator_close_download_button = (By.CSS_SELECTOR, "button.js-close:nth-child(3)")

locator_financial_totals = (By.CSS_SELECTOR, "#candidate-financial-totals > div:nth-child(2)")
locator_candidate_count = (By.CSS_SELECTOR, "#DataTables_Table_0_info")

locator_results_per_page = (By.CSS_SELECTOR, "#DataTables_Table_0_length > label:nth-child(1) > select:nth-child(1)")