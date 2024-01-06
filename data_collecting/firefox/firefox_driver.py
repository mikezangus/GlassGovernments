import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService

from .firefox_app_downloader import download_firefox_app
from .geckodriver_downloader import download_geckodriver

current_dir = os.path.dirname(os.path.abspath(__file__))
data_collecting_dir = os.path.dirname(current_dir)
project_dir = os.path.dirname(data_collecting_dir)
sys.path.append(project_dir)
from project_directories import load_data_dir, load_downloads_container_dir


firefox_binary_path = os.path.join(current_dir, "Firefox.app", "Contents", "MacOS", "firefox")
geckodriver_path = os.path.join(current_dir, "geckodriver")


def firefox_driver():

    data_dir = load_data_dir(project_dir)
    downloads_container_dir = load_downloads_container_dir(data_dir)
    
    if not os.path.isfile(firefox_binary_path):
        if not download_firefox_app():
            return False, None
    for file_name in os.listdir(current_dir):
        if file_name.lower().startswith("firefox_latest"):
            os.remove(os.path.join(current_dir, file_name))
    if not os.path.isfile(geckodriver_path):
        if not download_geckodriver():
            return False, None
    geckodriver_log_path = os.path.join(current_dir, "geckodriver.log")
    
    options = Options()
    options.binary_location = firefox_binary_path
    options.add_argument("--headless")
   
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("network.http.use-cache", False)

    options.set_preference("browser.download.alwaysOpenPanel", False)
    options.set_preference("browser.download.dir", downloads_container_dir)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.useDownloadDir", True)

    options.set_preference("layout.css.devPixelsPerPx", "1")

    service = FirefoxService(geckodriver_path, log_path = geckodriver_log_path)
    driver = webdriver.Firefox(options, service)
    
    driver.maximize_window()
    return True, driver