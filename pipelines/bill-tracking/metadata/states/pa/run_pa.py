from lib.insert_to_db import insert_to_db
from schemas.enums import Chamber, StateCode, OnDuplicate
from schemas.rows import BillMetadataRow
from states.pa.extract_metadata import extract_metadata
from states.pa.fetch_feed_entries import fetch_feed_entries
from states.pa.fetch_feed_pubdate import fetch_feed_pubdate
from states.pa.urls import lower_feed_url, upper_feed_url
from utils.trigger import trigger


def run_pa() -> None:
    state = StateCode.PA.value
    print(f"\n\nRunning bill metadata for {state}")
    trigger_lower = trigger(state, Chamber.LOWER, fetch_feed_pubdate)
    trigger_upper = trigger(state, Chamber.UPPER, fetch_feed_pubdate)
    if not trigger_lower and not trigger_upper:
        print(f"{state} has no feed updates")
        return
    feed_entries = []
    if trigger_lower:
        feed_entries.extend(fetch_feed_entries(lower_feed_url))
    if trigger_upper:
        feed_entries.extend(fetch_feed_entries(upper_feed_url))
    rows: list[BillMetadataRow] = []
    for feed_entry in feed_entries:
        rows.append(extract_metadata(feed_entry))
    insert_to_db("bill_metadata", rows, OnDuplicate.MERGE, "id")
