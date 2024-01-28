import os
import pandas as pd
import time

current_dir = os.path.dirname(os.path.abspath(__file__))
downloads_container_dir = os.path.join(current_dir, "downloads_container")
header_file_name = "indiv_header_file.csv"
header_file_path = os.path.join(current_dir, header_file_name)
main_file_name = "itcont24.txt"
main_file_path = os.path.join(current_dir, main_file_name)

with open(header_file_path, "r") as header_file:
    headers = header_file.readline().strip().split(",")

relevant_columns = [
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
relevant_column_indices = [headers.index(col) for col in relevant_columns]

try:
    start_time = time.time()
    print(f"\nLoading Committee ID dataframe\n")
    committee_id_index = headers.index("CMTE_ID")
    df_committee_ids = pd.read_csv(
        filepath_or_buffer = main_file_path,
        sep = "|",
        header = None,
        usecols = [0],
        verbose = True,
        on_bad_lines = "warn",
        low_memory = False
    )
    end_time = time.time()
    total_time = end_time - start_time
    committee_ids = df_committee_ids.iloc[:, 0].unique()
    committee_id_count = len(committee_ids)
    row_count = len(df_committee_ids)
    print(f"\nFininished loading Committee ID dataframe of {row_count:,} rows in {(total_time / 60):,.2f} minutes at {(row_count / (total_time / 60)):,.2f} rows per minute")
    print(f"Amount of unique committee IDs: {committee_id_count:,}")

    print("Loading full dataframe")
    start_time = time.time()
    df_full = pd.read_csv(
        filepath_or_buffer = main_file_path,
        sep ="|",
        header = None,
        names = headers,
        usecols = relevant_column_indices,
        verbose = True,
        on_bad_lines = "warn",
        low_memory = False
    )
    end_time = time.time()
    total_time = end_time - start_time
    row_count = len(df_full)
    print(f"\nFininished loading full dataframe of {row_count:,} rows in {(total_time / 60):,.2f} minutes at {(row_count / (total_time / 60)):,.2f} rows per minute")

    start_time = time.time()
    for i, committee_id in enumerate(committee_ids):
        df_filtered = df_full[df_full.iloc[:, 0] == committee_id]
        cleaned_file_name = f"{committee_id}_output.csv"
        cleaned_file_dir = os.path.join(current_dir, "2024")
        os.makedirs(cleaned_file_dir, exist_ok = True)
        cleaned_file_path = os.path.join(cleaned_file_dir, cleaned_file_name)
        df_filtered.to_csv(path_or_buf = cleaned_file_path, index = False)
        print(f"[{i:,}/{committee_id_count:,}] Finished processing Committee ID: {committee_id}\n{cleaned_file_path}\n")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Finished cleaning {committee_id_count:,} files in {(total_time / 60):,.2f} minutes at rate of {(committee_id_count / (total_time / 60)):,.2f} files per minute")

except Exception as e:
    print(f"Failed to load dataframe: {e}")