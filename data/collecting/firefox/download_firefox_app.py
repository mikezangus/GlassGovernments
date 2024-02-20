import os
import requests
import sys


def determine_os() -> tuple[str, str]:
    if sys.platform.startswith("linux"):
        url = "https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=linux64&lang=en-US"
        file_extension = ".tar.gz"
    elif sys.platform == "darwin":
        url = "https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=osx&lang=en-US"
        file_extension = ".dmg"
    elif sys.platform == "win32":
        url = "https://download.mozilla.org/?product=firefox-devedition-latest-ssl&os=win64&lang=en-US"
        file_extension = ".exe"
    else:
        raise Exception("Unsupported operating system")
    return url, file_extension


def download_app(dir: str, url: str, file_name: str, file_extension: str) -> bool:
    try:
        print(
            f"\nFirefox app isn't in the directory:\n{dir}"
            f"\n\nDownloading the Firefox app from Mozilla's official site:\n{url}"
        )
        response = requests.get(url)
        
        with open(file_name, "wb") as file:
            file.write(response.content)
        return True
    except Exception as e:
        print("Failed to download Firefox app. Error:", e)
        return False


def print_installation_instructions(file_extension: str, file_path: str, dir: str) -> None:
    print(
        f"\nSuccessfully downloaded the Firefox app"
        f"\n\n{'-' * 50}\nFIREFOX APP INSTALLATION INSTRUCTIONS:\n{'-' * 50}"
        f"\n1. Install the Firefox app by opening the {file_extension} file from the path:\n   {file_path}"
        f"\n2. Save the Firefox app to the EXACT directory:\n   {dir}/"
        f"\n3. Restart the data collection driver after installing and saving the Firefox app to the EXACT directory:\n   {dir}/"   
    )
    return


def install_app(file_name: str, dir: str):
    import tarfile
    if file_name.endswith(".tar.gz"):
        with tarfile.open(file_name) as tar:
            tar.extractall(path = dir)
        os.remove(file_name)
        print("Firefox app installed")
    return


def main() -> bool:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    url, file_extension = determine_os()
    file_name = os.path.join(current_dir, f"firefox_latest_dev{file_extension}")
    file_path = os.path.join(os.path.abspath(file_name))
    if not download_app(current_dir, url, file_name, file_extension):
        return False
    if sys.platform == "darwin" or sys.platform == "win32":
        print_installation_instructions(file_extension, file_path, current_dir)
        return False
    elif sys.platform == "linux":
        install_app(file_name, current_dir)
        return True
