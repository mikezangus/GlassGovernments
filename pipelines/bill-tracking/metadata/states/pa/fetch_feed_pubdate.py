from datetime import datetime, timezone
import feedparser
from schemas.enums import Chamber
from states.pa.urls import lower_feed_url, upper_feed_url


def fetch_feed_pubdate(chamber: Chamber) -> datetime:
    if chamber == Chamber.LOWER:
        url = lower_feed_url
    elif chamber == Chamber.UPPER:
        url = upper_feed_url
    else:
        raise ValueError("Invalid chamber")
    feed = feedparser.parse(url)
    feed_pubdate = getattr(feed.feed, "published_parsed", None)
    if not feed_pubdate:
        raise ValueError("Pubdate not found on feed")
    return datetime(*feed_pubdate[:6], tzinfo=timezone.utc).isoformat()
