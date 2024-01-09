import os
import pandas as pd


def load_file(subject, year: str, chamber: str, state: str, raw_file_name: str, raw_files_dir: str, district: str):
    relevant_cols = [
        "transaction_id",
        "entity_type_desc",
        "contributor_street_1",
        "contributor_city",
        "contributor_state",
        "contributor_zip",
        "contribution_receipt_date",
        "contribution_receipt_amount",
        "candidate_name",
        "candidate_office_full",
        "candidate_office_state",
        "candidate_office_district",
        "donor_committee_name",
        "fec_election_type_desc",
        "fec_election_year"
    ]
    if chamber.lower() == "house":
        raw_file_path = os.path.join(raw_files_dir, year, chamber, state, district, raw_file_name)
    elif chamber.lower() == "senate":
        raw_file_path = os.path.join(raw_files_dir, year, chamber, state, raw_file_name)
    try:
        data = pd.read_csv(
            filepath_or_buffer = raw_file_path,
            sep = ",",
            usecols = relevant_cols,
            dtype = str,
            na_values = "",
            keep_default_na = False,
            low_memory = False
        )
        data = data[data["fec_election_year"] == year]
        return data, True
    except pd.errors.EmptyDataError:
        print(f"{subject} | File is empty, moving on")
        return pd.DataFrame(), False
    except Exception as e:
        print(f"{subject} | Unexpected error occured. Error: {e}")
        return pd.DataFrame(), False