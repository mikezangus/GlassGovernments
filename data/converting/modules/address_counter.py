def count_addresses(data: object):
    data["full_address"] = data["contributor_street_1"] + ", " + data["contributor_city"] + ", " + data["contributor_state"] + " " + data["contributor_zip"]
    total_address_count = len(data["full_address"])
    print(total_address_count)
    return total_address_count