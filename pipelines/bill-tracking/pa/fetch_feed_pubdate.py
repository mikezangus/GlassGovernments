import feedparser
from datetime import datetime, timezone
from urls import lower_feed_url, upper_feed_url

import os
PA_DIR = os.path.dirname(os.path.abspath(__file__))
BILL_TRACKING_DIR = os.path.dirname(PA_DIR)

import sys
sys.path.append(BILL_TRACKING_DIR)
from chamber_type import Chamber


def fetch_feed_pubdate(chamber: Chamber) -> datetime:
    if chamber == Chamber.LOWER:
        url = lower_feed_url
    elif chamber == Chamber.UPPER:
        url = upper_feed_url
    else:
        raise ValueError()
    feed = feedparser.parse(url)
    feed_pubdate = feed.feed.get("published_parsed")
    return datetime(*feed_pubdate[:6], tzinfo=timezone.utc).isoformat()
