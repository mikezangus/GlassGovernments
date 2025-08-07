from schemas.enums import OnDuplicate, StateCode
from schemas.rows import BillMetadataRow
from states.oh.construct_search_url import construct_search_url
from states.oh.enums import LegislationType
from states.oh.extract_metadata import extract_metadata
from states.oh.get_bill_count import get_bill_count
from states.oh.get_bill_urls import get_bill_urls
from utils.insert_to_db import insert_to_db


SESSION = 136


def run_oh() -> None:
    state = StateCode.OH.value
    print(f"\n\nRunning bill metadata for {state}")
    bill_count = get_bill_count(SESSION)
    if bill_count < 1:
        print("No bills found")
        return
    search_urls = []
    for i in range(1, bill_count + 1, 1000):
        search_urls.append(construct_search_url(SESSION, i, 1000, list(LegislationType)))
    bill_urls = []
    for search_url in search_urls:
        bill_urls.extend(get_bill_urls(search_url))
    rows: list[BillMetadataRow] = []
    for bill_url in bill_urls:
        rows.append(extract_metadata(bill_url))
    insert_to_db("bill_metadata", rows, OnDuplicate.MERGE, "id")
