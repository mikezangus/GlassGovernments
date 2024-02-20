import os
import sys
import zipfile

modules_dir = os.path.dirname(os.path.abspath(__file__))
collecting_dir = os.path.dirname(modules_dir)
data_dir = os.path.dirname(collecting_dir)
sys.path.append(data_dir)
from directories import get_raw_year_dir


def unzip_files(election_year: str) -> bool:
    try:
        print("\nStarted unzipping all files")
        dir = get_raw_year_dir(election_year)
        for file_name in os.listdir(dir):
            if file_name.endswith(".zip"):
                print("Started unzipping", file_name)
                file_type = file_name[:-6]
                src_path = os.path.join(dir, file_name)
                dst_path = os.path.join(dir, file_type)
                with zipfile.ZipFile(src_path, "r") as z:
                    z.extractall(dst_path)
                    os.remove(src_path)
                    print("Finished unzipping", file_name)
        print("Finished unzipping all files")
        return True
    except Exception as e:
        print("Unzip Files | Error:", e)
        return False
