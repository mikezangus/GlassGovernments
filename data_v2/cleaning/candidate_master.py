import os
import pandas as pd
from pathlib import Path
import sys

current_dir = Path(__file__).resolve().parent
data_dir = str(current_dir.parent)
sys.path.append(data_dir)
from directories import get_raw_dir, get_cleaned_dir, get_headers_dir, get_src_file_dir


def decide_year() -> str:
    raw_dir = get_raw_dir()
    year_options = os.listdir(raw_dir)
    year_options = [y for y in year_options if y.isdigit()]
    sorted_year_options = sorted(
        year_options,
        key = lambda x: int(x)
    )
    formatted_year_options = ', '.join(sorted_year_options)
    while True:
        year = input(f"\nFor which year do you want to clean raw data?\nAvailable years: {formatted_year_options}\n> ")
        if year in year_options:
            return year
        else:
            print(f"\n{year} isn't an available year, try again")


def load_headers(file_type: str) -> list:
    headers_dir = get_headers_dir()
    header_file_path = os.path.join(headers_dir, f"{file_type}_header_file.csv")
    with open(header_file_path, "r") as header_file:
        headers = header_file.readline().strip().split(",")
    return headers


def set_cols(headers: list) -> list:
    relevant_cols = [
        "CAND_ID",
        "CAND_NAME",
        "CAND_PTY_AFFILIATION",
        "CAND_ELECTION_YR",
        "CAND_OFFICE_ST",
        "CAND_OFFICE",
        "CAND_OFFICE_DISTRICT",
        "CAND_ICI",
        "CAND_STATUS",
        "CAND_PCC"
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


def load_df(year: str, file_type: str, headers: list, cols: list) -> pd.DataFrame:
    src_file_dir = get_src_file_dir(year, file_type)
    src_file_path = os.path.join(src_file_dir, f"{file_type}.txt")
    df = pd.read_csv(
        filepath_or_buffer = src_file_path,
        sep = "|",
        header = None,
        names = headers,
        usecols = cols,
        dtype = str,
        verbose = True,
        on_bad_lines = "warn",
        low_memory = False
    )
    return df


def process_df(df: pd.DataFrame, year: str) -> pd.DataFrame:
    df = df[df["CAND_ELECTION_YR"] == year]
    df = df[df["CAND_STATUS"] == "C"]
    df = df.drop(columns = ["CAND_STATUS"])
    return df


def rename_cols(df: pd.DataFrame) -> pd.DataFrame:
    df.rename(
        columns = {
            "CAND_NAME": "NAME",
            "CAND_PTY_AFFILIATION": "PARTY",
            "CAND_ELECTION_YR": "ELECTION_YEAR",
            "CAND_OFFICE_ST": "STATE",
            "CAND_OFFICE": "OFFICE",
            "CAND_OFFICE_DISTRICT": "DISTRICT",
            "CAND_ICI": "ICI",
            "CAND_PCC": "CMTE_ID"
        },
        inplace= True
    )
    return df


def save_df(df: pd.DataFrame, year: str) -> None:
    cleaned_dir = get_cleaned_dir()
    dst_path = os.path.join(cleaned_dir, year)
    if not os.path.exists(dst_path):
        os.makedirs(dst_path, exist_ok = True)
    save_path = os.path.join(dst_path, "candidate_master.csv")
    df.to_csv(path_or_buf = save_path, index = False)
    print(f"File saved to path:\n{save_path}")
    return


def main():
    file_type = "cn"
    year = decide_year()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    df = load_df(year, file_type, headers, cols)
    df = process_df(df, year)
    df = rename_cols(df)
    save_df(df, year)


if __name__ == "__main__":
    main()