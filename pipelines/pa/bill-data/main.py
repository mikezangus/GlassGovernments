from fetch_feed_entries import fetch_feed_entries
from parse_actions import parse_actions
from parse_metadata import parse_metadata
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(PIPELINES_DIR)
from insert_to_db import insert_to_db, OnDuplicate
from urls import house_rss_url, senate_rss_url


def main():
    feed_entries = []
    for url in [house_rss_url, senate_rss_url]:
        feed_entries.extend(fetch_feed_entries(url))
    metadata_rows = []
    actions_rows = []
    for entry in feed_entries:
        metadata_rows.append(parse_metadata(entry))
        actions_rows.append(parse_actions(entry))
    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.IGNORE, "id")
    insert_to_db("bill_actions", actions_rows, OnDuplicate.MERGE, "id")


if __name__ == "__main__":
    main()
