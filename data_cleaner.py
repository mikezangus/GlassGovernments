import os
import pandas as pd

input_filename = "2022_PA_17_DELUZIO_CHRISTOPHER_DEMOCRATIC_source.csv"

candidate_info = input_filename.split("_")
year = candidate_info[0]
state = candidate_info[1]
district = candidate_info[2]
last_name = candidate_info[3]
first_name = candidate_info[4]
party = candidate_info[5]

output_filename = f"{year}_{state}_{district}_{last_name}_{first_name}_{party}_clean.csv"
relevant_columns = [
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
data = pd.read_csv(filepath_or_buffer = input_filename, sep = ",", usecols = relevant_columns)

data["contribution_receipt_date"] = pd.to_datetime(data["contribution_receipt_date"], errors = "coerce")

data.to_csv(output_filename, index = False)
