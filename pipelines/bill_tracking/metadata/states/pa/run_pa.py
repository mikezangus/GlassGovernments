from metadata.states.pa.fetch_feed_pubdate import fetch_feed_pubdate
from metadata.states.pa.parse_metadata_row import parse_metadata_row
from metadata.states.pa.urls import lower_feed_url, upper_feed_url
from metadata.utils.fetch_feed_entries import fetch_feed_entries
from metadata.utils.trigger import trigger
from shared.enums import Chamber, OnDuplicate, StateCode
from shared.rows import BillMetadataRow
from shared.utils.insert_to_db import insert_to_db


def run_pa() -> None:
    state = StateCode.PA
    print(f"\n\nRunning bill metadata for {state.value}")

    trigger_lower = trigger(state.value, Chamber.LOWER, fetch_feed_pubdate)
    trigger_upper = trigger(state.value, Chamber.UPPER, fetch_feed_pubdate)
    if not trigger_lower and not trigger_upper:
        print(f"{state.value} has no feed updates")
        return
    
    feed_entries = []
    if trigger_lower:
        feed_entries.extend(fetch_feed_entries(lower_feed_url))
    if trigger_upper:
        feed_entries.extend(fetch_feed_entries(upper_feed_url))
    
    metadata_rows: list[BillMetadataRow] = []
    for feed_entry in feed_entries:
        metadata_rows.append(parse_metadata_row(feed_entry, state.value))
        
    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.MERGE, ["id"])
