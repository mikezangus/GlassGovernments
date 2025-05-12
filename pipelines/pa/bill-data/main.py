from fetch_rss_entries import fetch_rss_entries
from parse_actions import parse_actions
from parse_metadata import parse_metadata
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(PIPELINES_DIR)
from insert_to_db import insert_to_db


rss_base_url = "https://legis.state.pa.us/WU01/LI/RSS/"
house_rss_url = rss_base_url + "HouseBills.xml"
senate_rss_url = rss_base_url + "SenateBills.xml"


def main():
    rss_entries = []
    for url in [house_rss_url, senate_rss_url]:
        rss_entries.extend(fetch_rss_entries(url))
    metadata_rows = []
    actions_rows = []
    for entry in rss_entries:
        metadata_rows.append(parse_metadata(entry))
        actions_rows.append(parse_actions(entry))
    insert_to_db("bill_metadata", metadata_rows)
    insert_to_db("bill_actions", actions_rows)


if __name__ == "__main__":
    main()
