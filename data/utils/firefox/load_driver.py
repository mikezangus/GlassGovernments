import os
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from .download_app import download_app as download_firefox_app
from .download_geckodriver import download_geckodriver as download_geckodriver


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))


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


def set_options(binary_path: str, headless: bool, download_dir: str = None) -> Options:
    options = Options()
    options.binary_location = binary_path
    if headless:
        options.add_argument("--headless")
    if download_dir is not None:
        options.set_preference("browser.download.alwaysOpenPanel", False)
        options.set_preference("browser.download.dir", download_dir)
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showAlertOnComplete", False)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.manager.useWindow", False)
        options.set_preference("browser.download.panel.shown", False)
        options.set_preference("browser.download.useDownloadDir", True)
    options.set_preference("browser.cache.disk.enable", False)
    options.set_preference("browser.cache.memory.enable", False)
    options.set_preference("browser.cache.offline.enable", False)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("network.http.use-cache", False)
    options.set_preference("layout.css.devPixelsPerPx", "1")
    return options


def create_driver(geckodriver_path: str, log_path: str, options: Options) -> webdriver.Firefox:
    service = Service(
        executable_path = geckodriver_path,
        log_path = log_path
    )
    driver = webdriver.Firefox(
        options = options,
        service = service
    )
    driver.maximize_window()
    return driver


def load_driver(headless: bool, download_dir: str = None) -> tuple[bool, webdriver.Firefox]:
    binary_path = os.path.join(CURRENT_DIR, "Firefox.app", "Contents", "MacOS", "firefox")
    geckodriver_path = os.path.join(CURRENT_DIR, "geckodriver")
    log_path = os.path.join(CURRENT_DIR, "geckodriver.log")
    if not verify_required_files(binary_path, CURRENT_DIR, geckodriver_path):
        return False, None
    options = set_options(binary_path, headless, download_dir)
    driver = create_driver(geckodriver_path, log_path, options)
    return True, driver
