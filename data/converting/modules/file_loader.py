import os
import pandas as pd


def load_file(subject, year: str, chamber: str, state: str, input_file_name: str, input_file_dir: str, district: str):

    if chamber.lower() == "house":
        input_file_path = os.path.join(input_file_dir, year, chamber, state, district, input_file_name)
    elif chamber.lower() == "senate":
        input_file_path = os.path.join(input_file_dir, year, chamber, state, input_file_name)

    try:
        data = pd.read_csv(
            filepath_or_buffer = input_file_path,
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