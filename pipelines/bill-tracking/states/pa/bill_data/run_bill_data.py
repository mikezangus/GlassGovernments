from states.pa.bill_data.fetch_feed_entries import fetch_feed_entries
from states.pa.bill_data.create_actions_row import create_actions_row
from states.pa.bill_data.create_metadata_row import create_metadata_row
from states.pa.urls import lower_feed_url, upper_feed_url
from schemas.enums import Chamber, OnDuplicate
from schemas.db_rows import BillMetadataRow, BillActionsRow
from insert_to_db import insert_to_db


def run_bill_data(chamber: Chamber) -> None:
    print("\n\nProcessing bill data")

    feed_entries = []
    if chamber == Chamber.LOWER:
        feed_entries.extend(fetch_feed_entries(lower_feed_url))
    if chamber == Chamber.UPPER:
        feed_entries.extend(fetch_feed_entries(upper_feed_url))

    metadata_rows: list[BillMetadataRow] = []
    actions_rows: list[BillActionsRow] = []
    for entry in feed_entries:
        metadata_rows.append(create_metadata_row(entry))
        actions_rows.append(create_actions_row(entry))

    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.IGNORE, "id")
    insert_to_db("bill_actions", actions_rows, OnDuplicate.MERGE, "id")
