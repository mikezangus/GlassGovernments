from fetch_guids import fetch_guids
from parse_guid import parse_guid
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(STATE_DIR))
from urls import house_rss_url, senate_rss_url
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(os.path.dirname(PIPELINES_DIR))
from insert_to_db import insert_to_db


def main():
    for url in [house_rss_url, senate_rss_url]:
        raw_guids = fetch_guids(url)
        guids = []
        for guid in raw_guids:
            parsed_guid = parse_guid(guid)
            guids.append(parsed_guid)
        insert_to_db("pa_bill_metadata", guids)


if __name__ == "__main__":
    main()
