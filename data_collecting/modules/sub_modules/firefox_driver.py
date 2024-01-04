import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options

from .firefox_driver_utilities.firefox_app_downloader import download_firefox_app
from .firefox_driver_utilities.geckodriver_downloader import download_geckodriver

current_dir = os.path.dirname(os.path.abspath(__file__))
data_collecting_modules_dir = os.path.dirname(current_dir)
data_collecting_dir = os.path.dirname(data_collecting_modules_dir)
project_dir = os.path.dirname(data_collecting_dir)
sys.path.append(project_dir)
from project_directories import load_data_dir, load_downloads_container_dir

firefox_driver_utilities_dir = os.path.join(current_dir, "firefox_driver_utilities")
firefox_binary_path = os.path.join(firefox_driver_utilities_dir, "Firefox.app", "Contents", "MacOS", "firefox")
geckodriver_path = os.path.join(firefox_driver_utilities_dir, "geckodriver")
data_dir = load_data_dir(project_dir)
downloads_container_dir = load_downloads_container_dir(data_dir)


def firefox_driver():
    
    if not os.path.isfile(firefox_binary_path):
        if not download_firefox_app():
            print(f"\nRestart the data collection driver after installing and saving the Firefox app to directory:\n{firefox_driver_utilities_dir}\n")
            return False, None
    if not os.path.isfile(geckodriver_path):
        if not download_geckodriver():
            return False, None
    for file_name in os.listdir(firefox_driver_utilities_dir):
        if file_name.lower().startswith("firefox_latest"):
            os.remove(os.path.join(firefox_driver_utilities_dir, file_name))
        
    geckodriver_log_path = os.path.join(firefox_driver_utilities_dir, "geckodriver.log")
    
    options = Options()
    options.binary = FirefoxBinary(firefox_binary_path)
    options.headless = True

    profile = webdriver.FirefoxProfile()
   
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("network.http.use-cache", False)

    profile.set_preference("browser.download.alwaysOpenPanel", False)
    profile.set_preference("browser.download.dir", downloads_container_dir)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.download.useDownloadDir", True)

    profile.set_preference("layout.css.devPixelsPerPx", "1")

    driver = webdriver.Firefox(
        firefox_profile = profile,
        executable_path = geckodriver_path,
        options = options,
        service_log_path = geckodriver_log_path
    )
    
    driver.maximize_window()
    return True, driver