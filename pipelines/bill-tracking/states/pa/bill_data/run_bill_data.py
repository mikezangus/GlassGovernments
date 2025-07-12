from states.pa.bill_data.fetch_feed_entries import fetch_feed_entries
from states.pa.bill_data.parse_actions import parse_actions
from states.pa.bill_data.parse_metadata import parse_metadata
from states.pa.urls import lower_feed_url, upper_feed_url
from enums import Chamber
from insert_to_db import insert_to_db, OnDuplicate


def run_bill_data(chamber: Chamber) -> None:
    print("\n\nProcessing bill data")
    feed_entries = []
    if chamber == Chamber.LOWER:
        feed_entries.extend(fetch_feed_entries(lower_feed_url))
    if chamber == Chamber.UPPER:
        feed_entries.extend(fetch_feed_entries(upper_feed_url))

    metadata_rows = []
    actions_rows = []
    for entry in feed_entries:
        metadata_rows.append(parse_metadata(entry))
        actions_rows.append(parse_actions(entry))

    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.IGNORE, "bill_id")
    insert_to_db("bill_actions", actions_rows, OnDuplicate.MERGE, "bill_id")
