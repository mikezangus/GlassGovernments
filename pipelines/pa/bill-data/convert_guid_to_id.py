def convert_guid_to_id(state: str, guid: str) -> str:
    guid_len = len(guid)
    guid_idx = 0    

    year = ""
    while guid_idx < 4 and guid[guid_idx].isdigit():
        year += guid[guid_idx]
        guid_idx += 1
    if len(year) == 0:
        raise ValueError

    session = ""
    while guid_idx < guid_len and guid[guid_idx].isdigit():
        session += guid[guid_idx]
        guid_idx += 1
    if len(session) == 0:
        raise ValueError

    bill_type = ""
    while guid_idx < guid_len and guid[guid_idx].isalpha():
        bill_type += guid[guid_idx]
        guid_idx += 1
    if len(bill_type) == 0:
        raise ValueError

    bill_num = ""
    while guid_idx < guid_len and guid[guid_idx].isdigit():
        bill_num += guid[guid_idx]
        guid_idx += 1
    if len(bill_num) == 0:
        raise ValueError

    print_num = ""
    while guid_idx < guid_len and guid[guid_idx].isalpha():
        guid_idx += 1
    while guid_idx < guid_len and guid[guid_idx].isdigit():
        print_num += guid[guid_idx]
        guid_idx += 1
    if len(print_num) == 0:
        raise ValueError

    return f"{state}_{year}_{session}_{bill_type}_{bill_num}_{print_num}"
