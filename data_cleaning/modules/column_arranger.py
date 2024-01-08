def arrange_columns(data):
    col_order = [
        "transaction_id",
        "election_year",
        "election_type",
        "election_state",
        "election_chamber",
        "election_constituency",
        "candidate_last_name",
        "candidate_first_name",
        "candidate_party",
        "contribution_date",
        "contribution_entity",
        "contribution_latitude",
        "contribution_longitude",
        "contribution_amount",
        "contributor_office_full",
        "contributor_office_state",
        "contributor_office_district"
    ]
    data = data.reindex(columns = col_order)
    return data