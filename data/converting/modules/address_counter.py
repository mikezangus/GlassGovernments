def count_addresses(data: object):
    data["full_address"] = data["contribution_street"] + ", " + data["contribution_city"] + ", " + data["contribution_state"] + " " + data["contribution_zip"]
    total_address_count = len(data["full_address"])
    return total_address_count