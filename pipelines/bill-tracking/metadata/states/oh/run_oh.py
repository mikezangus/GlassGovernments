from states.oh.get_bill_count import get_bill_count
from states.oh.construct_search_url import construct_search_url
from states.oh.get_bill_urls import get_bill_urls
from states.oh.extract_metadata_from_bill_url import extract_metadata_from_bill_url
from states.oh.create_row import create_row
from states.oh.enums import LegislationType
from lib.insert_to_db import insert_to_db
from schemas.rows import BillMetadataRow
from schemas.enums import OnDuplicate, StateCode


SESSION = 136


def run_oh() -> None:
    state = StateCode.OH.value
    print(f"\n\nRunning bill metadata for {state}")
    bill_count = get_bill_count(SESSION)
    search_urls = []
    for i in range(1, bill_count + 1, 1000):
        search_urls.append(construct_search_url(SESSION, i, 1000, list(LegislationType)))
    bill_urls = []
    for search_url in search_urls:
        bill_urls.extend(get_bill_urls(search_url))
    rows: list[BillMetadataRow] = []
    for bill_url in bill_urls:
        metadata = extract_metadata_from_bill_url(bill_url)
        rows.append(create_row(metadata))
    insert_to_db("bill_metadata", rows, OnDuplicate.MERGE, "id")
