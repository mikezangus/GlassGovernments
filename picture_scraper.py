from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.headless = False
driver_path = "scraper/geckodriver"
log_path = "scraper/geckodriver.log"
driver = webdriver.Firefox(executable_path = driver_path, service_log_path = log_path, options = options)
search_engine = "https://duckduckgo.com"
driver.get(search_engine)

def click_element(element):
    driver.execute_script("arguments[0].scrollIntoView();", element)
    element.click()

politician_name = input("Input politician's name: ")
politician_state = input("Input politician's state: ")

search_bar = driver.find_element_by_css_selector("#searchbox_input")
click_element(search_bar)

search_bar.send_keys(f'"politician" "{politician_name}" {politician_state}')
search_button = driver.find_element_by_css_selector(".searchbox_searchButton__F5Bwq")
click_element(search_button)

wikipedia_url = driver.find_element_by_css_selector("a[href*='.wikipedia.org'][data-testid='result-title-a']:first-child")
click_element(wikipedia_url)

partial_image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".infobox-image")))
click_element(partial_image_element)

full_image_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".mw-mmv-final-image")))
politician_image_url = full_image_element.get_attribute("src")
print(politician_image_url)