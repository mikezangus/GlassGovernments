from schemas.rows import BillMetadataRow
from states.pa.create_id import create_id


def create_row(feed_entry: dict[str, any]) -> BillMetadataRow:
    id = create_id(feed_entry["id"])
    state, session, special_session, type, bill_num, print_num = id.split('_')
    return {
        "id": id,
        "state": state,
        "session": int(session),
        "special_session": int(special_session),
        "type": type,
        "bill_num": int(bill_num),
        "print_num": int(print_num),
        "bill_url": f"https://www.palegis.us/legislation/bills/{session}/{type}{bill_num}",
        "text_url": feed_entry["link"],
    }
