import os
import requests
import sys
import tarfile
import zipfile


def determine_url() -> str | None:
    github_response = requests.get(
        "https://api.github.com/repos/mozilla/geckodriver/releases/latest"
    )
    latest_version = github_response.json()["tag_name"]
    base_url = (
        "https://github.com/mozilla/geckodriver/releases/download/"
        f"{latest_version}/"
    )
    if sys.platform.startswith("linux"):
        url = base_url + "geckodriver-" + latest_version + "-linux64.tar.gz"
    elif sys.platform == "darwin":
        url = base_url + "geckodriver-" + latest_version + "-macos.tar.gz"
    elif sys.platform == "win32":
        url = base_url + "geckodriver-" + latest_version + "-win64.zip"
    else:
        raise Exception("Unsupported operating system")
        return
    return url


def download_file(url: str) -> tuple[bool, str]:
    print(f"\nStarting to download Geckodriver from Mozilla's official GitHub repository:\n{url}")
    try:
        geckodriver_response = requests.get(url)
        file_name = url.split("/")[-1]
        with open(file_name, "wb") as file:
            file.write(geckodriver_response.content)
        print("Successfully downloaded Geckodriver")
        return True, file_name
    except Exception as e:
        print("Failed to download Geckodriver. Error:", e)
        return False, None


def install_file(file_name: str) -> bool:
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"\nStarting to install Geckodriver to:\n{current_dir}")
        if file_name.endswith(".tar.gz"):
            with tarfile.open(file_name) as tar:
                tar.extractall(current_dir)
        elif file_name.endswith(".zip"):
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(current_dir)
        os.remove(file_name)
        print(f"Successfully installed Geckodriver to:\n{current_dir}")
        return True
    except Exception as e:
        print("Failed to install Geckodriver. Error:", e)
        return False


def main() -> bool:
    if determine_url() is not None:
        url = determine_url()
    success, file_name = download_file(url)
    if not success:
        return False
    elif not install_file(file_name):
        return False
    return True
