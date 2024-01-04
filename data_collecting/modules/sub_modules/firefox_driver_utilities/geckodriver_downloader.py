import os
import requests
import sys
import tarfile
import zipfile


def download_geckodriver():

    try:

        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        response = requests.get("https://api.github.com/repos/mozilla/geckodriver/releases/latest")
        latest_version = response.json()["tag_name"]
        url = f"https://github.com/mozilla/geckodriver/releases/download/{latest_version}/"

        if sys.platform.startswith("linux"):
            url += "geckodriver-" + latest_version + "-linux64.tar.gz"
        elif sys.platform == "darwin":
            url += "geckodriver-" + latest_version + "-macos.tar.gz"
        elif sys.platform == "win32":
            url += "geckodriver-" + latest_version + "-win64.zip"
        else:
            raise Exception("Unsupported operating system")

        geckodriver_response = requests.get(url)
        geckodriver_filename = url.split("/")[-1]
        print(f"Installing {geckodriver_filename} from {url}")
        with open(geckodriver_filename, "wb") as file:
            file.write(geckodriver_response.content)
        
        if geckodriver_filename.endswith(".tar.gz"):
            with tarfile.open(geckodriver_filename) as tar:
                tar.extractall(current_dir)
        elif geckodriver_filename.endswith(".zip"):
            with zipfile.ZipFile(geckodriver_filename, "r") as zip_ref:
                zip_ref.extractall(current_dir)

        os.remove(geckodriver_filename)

        return True

    except:
        print("Failed to install geckodriver")
        return False