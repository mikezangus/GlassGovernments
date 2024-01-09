import os
import pandas as pd


def load_file(subject, year: str, chamber: str, state: str, cleaned_file_name: str, cleaned_files_dir: str, district: str):

    if chamber.lower() == "house":
        cleaned_file_path = os.path.join(cleaned_files_dir, year, chamber, state, district, cleaned_file_name)
    elif chamber.lower() == "senate":
        cleaned_file_path = os.path.join(cleaned_files_dir, year, chamber, state, cleaned_file_name)

    try:
        data = pd.read_csv(
            filepath_or_buffer = cleaned_file_path,
            sep = ",",
            dtype = str
        )
        return data, True
    except pd.errors.EmptyDataError:
        print(f"{subject} | File is empty, moving on")
        return pd.DataFrame(), False
    except Exception as e:
        print(f"{subject} | Unexpected error occured. Error: {e}")
        return pd.DataFrame(), False