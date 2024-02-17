import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from .firefox_app_downloader import download_firefox_app
from .geckodriver_downloader import download_geckodriver


def set_options(binary_path: str, downloads_dir: str) -> Options:

    options = Options()
    options.binary_location = binary_path

    # options.add_argument("--headless")
   
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("network.http.use-cache", False)

    options.set_preference("browser.download.alwaysOpenPanel", False)
    options.set_preference("browser.download.dir", downloads_dir)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.useDownloadDir", True)

    options.set_preference("layout.css.devPixelsPerPx", "1")

    return options


def firefox_driver(downloads_dir: str) -> tuple[bool, webdriver.Firefox]:

    app_dir = os.path.dirname(os.path.abspath(__file__))
    binary_path = os.path.join(app_dir, "Firefox Developer Edition.app", "Contents", "MacOS", "firefox")
    geckodriver_path = os.path.join(app_dir, "geckodriver")
    
    if not os.path.isfile(binary_path):
        if not download_firefox_app():
            return False, None
    for file_name in os.listdir(app_dir):
        if file_name.lower().startswith("firefox_latest"):
            os.remove(os.path.join(app_dir, file_name))
    if not os.path.isfile(geckodriver_path):
        if not download_geckodriver():
            return False, None
    geckodriver_log_path = os.path.join(app_dir, "geckodriver.log")
    
    options = set_options(binary_path, downloads_dir)

    driver = webdriver.Firefox(
        executable_path = geckodriver_path, options = options, log_path = geckodriver_log_path
    )
    
    driver.maximize_window()
    return True, driver
