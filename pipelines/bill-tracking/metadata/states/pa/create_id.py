def create_id(guid: str) -> str:
    guid_len = len(guid)
    guid_idx = 0    

    session = ""
    while guid_idx < 4 and guid[guid_idx].isdigit():
        session += guid[guid_idx]
        guid_idx += 1
    if len(session) == 0:
        raise ValueError

    special_session = ""
    while guid_idx < guid_len and guid[guid_idx].isdigit():
        special_session += guid[guid_idx]
        guid_idx += 1
    if len(special_session) == 0:
        raise ValueError

    type = ""
    while guid_idx < guid_len and guid[guid_idx].isalpha():
        type += guid[guid_idx]
        guid_idx += 1
    if len(type) == 0:
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

    return f"PA_{session}_{special_session}_{type}_{bill_num}_{print_num}"
