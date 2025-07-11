from fetch_feed_entries import fetch_feed_entries
from parse_actions import parse_actions
from parse_metadata import parse_metadata

import os
BILL_DATA_DIR = os.path.dirname(os.path.abspath(__file__))
PA_DIR = os.path.dirname(BILL_DATA_DIR)
BILL_TRACKING_DIR = os.path.dirname(PA_DIR)
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)

import sys
sys.path.append(PIPELINES_DIR)
from enums import Chamber
from insert_to_db import insert_to_db, OnDuplicate
from urls import lower_feed_url, upper_feed_url


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
