import os
import pandas as pd
from pathlib import Path
import sys
import time

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
        "CMTE_ID",
        "AMNDT_IND",
        "RPT_TP",
        "TRANSACTION_PGI",
        "TRANSACTION_TP",
        "ENTITY_TP",
        "CITY",
        "STATE",
        "ZIP_CODE",
        "TRANSACTION_DT",
        "TRANSACTION_AMT",
        "OTHER_ID",
        "TRAN_ID",
        "FILE_NUM",
    ]
    relevant_cols_indices = [headers.index(c) for c in relevant_cols]
    return relevant_cols_indices


def load_committees(year: str, file_type: str) -> list | None:
    try:
        start_time = time.time()
        print(f"\nStarted loading Committees DataFrame at {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        src_file_dir = get_src_file_dir(year, file_type)
        src_file_path = os.path.join(src_file_dir, f"itcont.txt")
        df = pd.read_csv(
            filepath_or_buffer = src_file_path,
            sep = "|",
            header = None,
            usecols = [0],
            verbose = True,
            on_bad_lines = "warn",
            low_memory = False
        )
        row_count = len(df)
        committees = df.iloc[:, 0].unique()
        committee_count = len(committees)
        total_time = (time.time() - start_time) / 60
        print("\nFinished loading Committees DataFrame:")
        print(f"Duration: {total_time:,.2f} minutes")
        print(f"Row count: {row_count:,}")
        print(f"Committee count: {committee_count:,}")
        print(f"Rate: {(row_count / total_time):,.2f} rows per minute\n")
        return committees
    except Exception as e:
        print(f"\nFailed to load Committees DataFrame. Error: {e}")
        return None


def load_df(year: str, file_type: str, headers: list, cols: list) -> pd.DataFrame | None:
    try:
        print("Headers:", headers)
        print("Columns:", cols)
        start_time = time.time()
        print(f"\nStarted to load DataFrame at {time.strftime('%H:%M:%S', time.localtime(start_time))}")
        src_file_dir = get_src_file_dir(year, file_type)
        src_file_path = os.path.join(src_file_dir, f"itcont.txt")
        df = pd.read_csv(
            filepath_or_buffer = src_file_path,
            sep = "|",
            header = None,
            names = headers,
            usecols = cols,
            verbose = True,
            on_bad_lines = "warn",
            low_memory = False
        )
        total_time = (time.time() - start_time) / 60
        row_count = len(df)
        print("\nFinished loading Full DataFrame:")
        print(f"Duration: {total_time:,.2f} minutes")
        print(f"Row count: {row_count:,}")
        print(f"Rate: {(row_count / total_time):,.2f} rows per minute\n")
        return df
    except Exception as e:
        print(f"\nFailed to load Full DataFrame. Error: {e}")
        return None


def save_df(df: pd.DataFrame, year: str, committee: str) -> str:
    cleaned_dir = get_cleaned_dir()
    dst_dir = os.path.join(cleaned_dir, year, "contributions_individuals")
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir, exist_ok = True)
    dst_path = os.path.join(dst_dir, f"{committee}.csv")
    df.to_csv(path_or_buf = dst_path, index = False)
    return dst_path


def process_df(df: pd.DataFrame, year: str, committees: list) -> None:
    start_time = time.time()
    print(f"\nStarted to process DataFrame at {time.strftime('%H:%M:%S', time.localtime(start_time))}")
    committee_count = len(committees)
    for i, committee in enumerate(committees):
        df_committee = df[df.iloc[:, 0] == committee]
        path = save_df(df_committee, year, committee)
        print(f"\n[{(i + 1):,}/{committee_count:,}] Saved to path:\n{path}")
    total_time = (time.time() - start_time) / 60
    print("\nFinished processing committee files:")
    print(f"Duration: {total_time:,.2f} minutes")
    print(f"File count: {committee_count:,}")
    print(f"Rate: {(committee_count / total_time):,.2f} files per minute\n")
    return


def main():
    file_type = "indiv"
    year = decide_year()
    headers = load_headers(file_type)
    cols = set_cols(headers)
    committees = load_committees(year, file_type)
    df = load_df(year, file_type, headers, cols)
    process_df(df, year, committees)


if __name__ == "__main__":
    main()