from schemas.enums import StateCode, OnDuplicate
from schemas.rows import BillMetadata
from states.wi.extract_metadata import extract_metadata
from states.wi.urls import lower_feed_url, upper_feed_url
from utils.fetch_feed_entries import fetch_feed_entries
from utils.insert_to_db import insert_to_db


def run_wi() -> None:
    state = StateCode.WI.value
    print(f"\n\nRunning bill metadata for {state}")
    feed_entries = []
    feed_entries.extend(fetch_feed_entries(lower_feed_url))
    feed_entries.extend(fetch_feed_entries(upper_feed_url))
    rows: list[BillMetadata] = []
    for feed_entry in feed_entries:
        rows.append(extract_metadata(feed_entry, state))
    insert_to_db("bill_metadata", rows, OnDuplicate.MERGE, "id")
