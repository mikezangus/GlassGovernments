import feedparser
from datetime import datetime, timezone
from urls import house_rss_url, senate_rss_url
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db
from insert_to_db import insert_to_db, OnDuplicate


def main():
    house_feed = feedparser.parse(house_rss_url)
    house_pubdate_raw = house_feed.feed.get("published_parsed")
    house_pubdate = datetime(
        *house_pubdate_raw[:6],
        tzinfo=timezone.utc
    ).isoformat()
    senate_feed = feedparser.parse(senate_rss_url)
    senate_pubdate_raw = senate_feed.feed.get("published_parsed")
    senate_pubdate = datetime(
        *senate_pubdate_raw[:6],
        tzinfo=timezone.utc
    ).isoformat()
    last_house_pubdate_row = fetch_from_db(
        "feed_updates",
        {
            "select": "pubdate",
            "chamber": "eq.house"
        }
    )
    last_senate_pubdate_row = fetch_from_db(
        "feed_updates",
        {
            "select": "pubdate",
            "chamber": "eq.senate"
        }
    )
    last_house_pubdate = None
    if last_house_pubdate_row:
        last_house_pubdate = last_house_pubdate_row[0]["pubdate"]
    last_senate_pubdate = None
    if last_senate_pubdate_row:
        last_senate_pubdate = last_senate_pubdate_row[0]["pubdate"]
    if not last_house_pubdate or house_pubdate > last_house_pubdate:
        insert_to_db(
            "feed_updates",
            [{ "chamber": "house", "pubdate": house_pubdate }],
            OnDuplicate.MERGE,
            "chamber"
        )
    if not last_senate_pubdate or senate_pubdate > last_senate_pubdate:
        insert_to_db(
            "feed_updates",
            [{ "chamber": "senate", "pubdate": senate_pubdate }],
            OnDuplicate.MERGE,
            "chamber"
        )
        

if __name__ == "__main__":
    main()
