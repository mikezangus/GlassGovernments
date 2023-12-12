import os
import sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def firefox_driver():
    
    options = Options()
    options.headless = False

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.privatebrowsing.autostart", True)
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    profile.set_preference("layout.css.devPixelsPerPx", "1")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    sys.path.append(parent_dir)
    from directories import downloads_container_dir

    profile.set_preference("browser.download.dir", downloads_container_dir)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.useDownloadDir", True)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.download.manager.closeWhenDone", True)
    profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    profile.set_preference("browser.download.manager.flashCount", 0)
    profile.set_preference("browser.download.manager.focusWhenStarting", False)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)

    driver = webdriver.Firefox(
        executable_path = os.path.join(current_dir, "firefox_driver_utilities", "geckodriver"),
        service_log_path = os.path.join(current_dir, "firefox_driver_utilities", "geckodriver.log"),
        options = options,
        firefox_profile = profile
    )

    driver.maximize_window()
    return driver