import os
import requests
import sys


def download_firefox_app():
    
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if sys.platform.startswith("linux"):
        url = "https://download.mozilla.org/?product=firefox-latest&os=linux64&lang=en-US"
        file_extension = ".tar.gz"
    elif sys.platform == "darwin":
        url = "https://download.mozilla.org/?product=firefox-latest&os=osx&lang=en-US"
        file_extension = ".dmg"
    elif sys.platform == "win32":
        url = "https://download.mozilla.org/?product=firefox-latest&os=win64&lang=en-US"
        file_extension = ".exe"
    else:
        raise Exception("Unsupported operating system")

    firefox_file_name = os.path.join(current_dir, f"firefox_latest{file_extension}")
    firefox_file_path = os.path.join(os.path.abspath(firefox_file_name))

    print(f"\nThe Firefox app isn't in directory:\n{current_dir}")
    print(f"\nDownloading the Firefox app from Mozilla's official site:\n{url}")
    response = requests.get(url)

    with open(firefox_file_name, "wb") as file:
        file.write(response.content)

    if sys.platform == "darwin" or sys.platform == "win32":
        print(f"\nSuccessfully downloaded the Firefox app, install by opening it from path:\n{firefox_file_path}\nThen save the Firefox app to directory:\n{current_dir}")
        return False
    elif sys.platform == "linux":
        import tarfile
        if firefox_file_name.endswith(".tar.gz"):
            with tarfile.open(firefox_file_name) as tar:
                tar.extractall(path=current_dir)
            os.remove(firefox_file_name)
            print("Firefox downloaded and extracted")
            return True