import feedparser
from feedparser import FeedParserDict


def fetch_feed_entries(url: str) -> list[FeedParserDict]:
    feed = feedparser.parse(url)
    return list(feed.entries)
