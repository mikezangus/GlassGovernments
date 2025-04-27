import feedparser


def fetch_guids(url: str) -> list[dict[str, str]]:
    feed = feedparser.parse(url)
    guids = []
    for entry in feed.entries:
        guid = entry.get("guid")
        guids.append(guid)
    return guids
