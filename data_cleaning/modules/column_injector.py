def inject_columns(data, state: str, chamber: str, district: str, last_name: str, first_name: str, party: str):
    data["election_state"] = state
    data["election_chamber"] = chamber
    data["election_constituency"] = district
    data["candidate_last_name"] = last_name
    data["candidate_first_name"] = first_name
    data["candidate_party"] = party
    return data