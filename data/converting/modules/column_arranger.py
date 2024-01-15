def arrange_columns(data: object):
    column_order = [
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
        "contribution_amount",
        "contribution_latitude",
        "contribution_longitude",
        "contribution_office_full",
        "contribution_office_state",
        "contribution_office_district"
    ]
    data = data.reindex(columns = column_order)
    return data