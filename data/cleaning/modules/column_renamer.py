def rename_columns(data: object):
    data["election_year"] = data["fec_election_year"]
    data["election_type"] = data["fec_election_type_desc"]
    data["contribution_date"] = data["contribution_receipt_date"]
    data["contribution_entity"] = data["entity_type_desc"]
    data["contribution_amount"] = data["contribution_receipt_amount"]
    data["contributor_office_full"] = data["candidate_office_full"]
    data["contributor_office_state"] = data["candidate_office_state"]
    data["contributor_office_district"] = data["candidate_office_district"]
    return data