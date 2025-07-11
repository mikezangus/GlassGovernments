from convert_guid_to_id import convert_guid_to_id


def parse_metadata(entry: dict[str, any]) -> dict[str, any]:
    id = convert_guid_to_id("PA", entry["id"])
    state, year, session, bill_type, bill_num, print_num = id.split('_')
    return {
        "bill_id": id,
        "state": state,
        "year": int(year),
        "session": int(session),
        "bill_type": bill_type,
        "bill_num": int(bill_num),
        "print_num": int(print_num),
        "text_url": entry["link"],
        "summary": entry["summary"]
    }
