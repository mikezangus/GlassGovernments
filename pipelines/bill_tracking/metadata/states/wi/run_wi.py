from .parse_metadata_row import parse_metadata_row
from .urls import lower_feed_url, upper_feed_url
from ...utils.fetch_feed_entries import fetch_feed_entries
from ....shared.enums import StateCode, OnDuplicate
from ....shared.rows import BillMetadataRow
from .....db.utils.insert import insert


def run_wi() -> None:
    state = StateCode.WI.value
    print(f"\n\nRunning bill metadata for {state}")

    feed_entries = []
    feed_entries.extend(fetch_feed_entries(lower_feed_url))
    feed_entries.extend(fetch_feed_entries(upper_feed_url))

    metadata_rows: list[BillMetadataRow] = []
    for feed_entry in feed_entries:
        metadata_rows.append(parse_metadata_row(feed_entry, state))
        
    insert("bill_metadata", metadata_rows, OnDuplicate.MERGE, ["id"])
