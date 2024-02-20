import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from .download_firefox_app import main as download_firefox_app
from .download_geckodriver import main as download_geckodriver


def verify_required_files(binary_path: str, app_dir: str, geckodriver_path: str) -> bool:
    if not os.path.isfile(binary_path):
        if not download_firefox_app():
            return False
    for file_name in os.listdir(app_dir):
        if file_name.lower().startswith("firefox_latest"):
            os.remove(os.path.join(app_dir, file_name))
    if not os.path.isfile(geckodriver_path):
        if not download_geckodriver():
            return False
    return True


def set_options(binary_path: str, download_dir: str, headless: bool) -> Options:

    options = Options()
    options.binary_location = binary_path
   
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("network.http.use-cache", False)

    options.set_preference("browser.download.alwaysOpenPanel", False)
    options.set_preference("browser.download.dir", download_dir)
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.manager.showAlertOnComplete", False)
    options.set_preference("browser.download.manager.showWhenStarting", False)
    options.set_preference("browser.download.manager.useWindow", False)
    options.set_preference("browser.download.panel.shown", False)
    options.set_preference("browser.download.useDownloadDir", True)

    options.set_preference("layout.css.devPixelsPerPx", "1")

    if headless:
        options.add_argument("--headless")

    return options


def load_driver(geckodriver_path: str, options: Options, geckodriver_log_path: str) -> webdriver.Firefox:
    driver = webdriver.Firefox(
        executable_path = geckodriver_path,
        options = options,
        log_path = geckodriver_log_path
    )
    driver.maximize_window()
    return driver


def main(download_dir: str, headless: bool) -> tuple[bool, webdriver.Firefox]:
    firefox_dir = os.path.dirname(os.path.abspath(__file__))
    binary_path = os.path.join(firefox_dir, "Firefox Developer Edition.app", "Contents", "MacOS", "firefox")
    geckodriver_path = os.path.join(firefox_dir, "geckodriver")
    geckodriver_log_path = os.path.join(firefox_dir, "geckodriver.log")
    if not verify_required_files(binary_path, firefox_dir, geckodriver_path):
        return False, None
    options = set_options(binary_path, download_dir, headless)
    driver = load_driver(geckodriver_path, options, geckodriver_log_path)
    return True, driver
