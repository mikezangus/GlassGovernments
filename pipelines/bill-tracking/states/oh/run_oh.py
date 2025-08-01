from states.oh.get_bill_count import get_bill_count
from states.oh.construct_search_url import construct_search_url
from states.oh.get_bill_urls import get_bill_urls
from states.oh.extract_metadata_from_bill_url import extract_metadata_from_bill_url
from states.oh.construct_bill_id import construct_bill_id
from states.oh.enums import LegislationType
from insert_to_db import insert_to_db, OnDuplicate


STATE = "OH"
SESSION = 136


def run_oh():
    bill_count = get_bill_count(SESSION)
    search_urls = []
    for i in range(1, bill_count + 1, 1000):
        search_urls.append(construct_search_url(SESSION, i, 1000, list(LegislationType)))
    bill_urls = []
    for search_url in search_urls:
        bill_urls.extend(get_bill_urls(search_url))
    metadata_rows = []
    for bill_url in bill_urls:
        state, session, bill_type, bill_num = extract_metadata_from_bill_url(bill_url)
        bill_id = construct_bill_id(state, session, bill_type, bill_num)
        metadata_rows.append({
            "bill_id": bill_id,
            "state": state,
            "session": session,
            "bill_type": bill_type,
            "bill_num": bill_num,
            "bill_url": bill_url
        })
    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.IGNORE, "bill_id")


if __name__ == "__main__":
    run_oh()
