from metadata.states.wi.parse_metadata_row import parse_metadata_row
from metadata.states.wi.urls import lower_feed_url, upper_feed_url
from metadata.utils.fetch_feed_entries import fetch_feed_entries
from shared.enums import StateCode, OnDuplicate
from shared.rows import BillMetadataRow
from shared.utils.insert_to_db import insert_to_db


def run_wi() -> None:
    state = StateCode.WI.value
    print(f"\n\nRunning bill metadata for {state}")

    feed_entries = []
    feed_entries.extend(fetch_feed_entries(lower_feed_url))
    feed_entries.extend(fetch_feed_entries(upper_feed_url))

    metadata_rows: list[BillMetadataRow] = []
    for feed_entry in feed_entries:
        metadata_rows.append(parse_metadata_row(feed_entry, state))
        
    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.MERGE, ["id"])
