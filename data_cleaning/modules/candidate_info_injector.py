def inject_candidate_info(data, state, district, last_name, first_name, party):
    data["candidate_state"] = state
    data["candidate_district"] = district
    data["candidate_last_name"] = last_name
    data["candidate_first_name"] = first_name
    data["candidate_party"] = party
    return data