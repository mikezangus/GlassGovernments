def parse_guid(guid: str) -> dict[str, str]:

    guid_len = len(guid)
    i = 0

    year = ""
    while i < 4 and guid[i].isdigit():
        year += guid[i]
        i += 1
    if len(year) == 0:
        raise ValueError

    session = ""
    while i < guid_len and guid[i].isdigit():
        session += guid[i]
        i += 1
    if len(session) == 0:
        raise ValueError

    bill_type = ""
    while i < guid_len and guid[i].isalpha():
        bill_type += guid[i]
        i += 1
    if len(bill_type) == 0:
        raise ValueError

    bill_num = ""
    while i < guid_len and guid[i].isdigit():
        bill_num += guid[i]
        i += 1
    if len(bill_num) == 0:
        raise ValueError

    print_num = ""
    while i < guid_len and guid[i].isalpha():
        i += 1
    while i < guid_len and guid[i].isdigit():
        print_num += guid[i]
        i += 1
    if len(print_num) == 0:
        raise ValueError

    return {
        "id": guid,
        "year": year,
        "session": session,
        "bill_type": bill_type,
        "bill_num": bill_num,
        "print_num": print_num
    }
