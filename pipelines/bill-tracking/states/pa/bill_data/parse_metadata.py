from states.pa.bill_data.convert_guid_to_id import convert_guid_to_id


def parse_metadata(entry: dict[str, any]) -> dict[str, any]:
    id = convert_guid_to_id("PA", entry["id"])
    print(entry["id"])
    state, session, special_session, bill_type, bill_num, print_num = id.split('_')
    return {
        "bill_id": id,
        "state": state,
        "session": int(session),
        "special_session": int(special_session),
        "bill_type": bill_type,
        "bill_num": int(bill_num),
        "print_num": int(print_num),
        "bill_url": f"https://www.palegis.us/legislation/bills/{session}/{bill_type}{bill_num}",
        "text_url": entry["link"],
    }
