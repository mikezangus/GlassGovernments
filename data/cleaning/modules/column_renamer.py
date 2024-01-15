def rename_columns(data: object):
    data["election_year"] = data["fec_election_year"]
    data["election_type"] = data["fec_election_type_desc"]
    data["contribution_date"] = data["contribution_receipt_date"]
    data["contribution_entity"] = data["entity_type_desc"]
    data["contribution_amount"] = data["contribution_receipt_amount"]
    data["contribution_street"] = data["contributor_street_1"]
    data["contribution_city"] = data["contributor_city"]
    data["contribution_state"] = data["contributor_state"]
    data["contribution_zip"] = data["contributor_zip"]
    data["contribution_office_full"] = data["candidate_office_full"]
    data["contribution_office_state"] = data["candidate_office_state"]
    data["contribution_office_district"] = data["candidate_office_district"]
    return data