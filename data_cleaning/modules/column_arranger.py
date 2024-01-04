def arrange_columns(data):
    col_order = [
        "transaction_id",
        "candidate_last_name",
        "candidate_first_name",
        "fec_election_year",
        "candidate_state",
        "candidate_district",
        "candidate_party",
        "contribution_receipt_date",
        "contribution_receipt_amount",
        "entity_type_desc",
        "contribution_latitude",
        "contribution_longitude",
        "fec_election_type_desc",
        "donor_committee_name",
        "candidate_office_full",
        "candidate_office_state",
        "candidate_office_district"
    ]
    data = data.reindex(columns = col_order)
    return data