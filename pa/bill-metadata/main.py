import os
import sys
from fetch_guids import fetch_guids
from parse_guid import parse_guid
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from insert_to_db import insert_to_db
from urls import house_rss_url, senate_rss_url


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
