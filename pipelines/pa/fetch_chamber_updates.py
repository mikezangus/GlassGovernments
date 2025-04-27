import feedparser
from urls import house_rss_url, senate_rss_url


HOUSE_PUBDATE_FILE_NAME = "last_pubdate_house.txt"
SENATE_PUBDATE_FILE_NAME = "last_pubdate_senate.txt"


def read_pubdate(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return f.read().strip()


def write_pubdate(file_name: str, pubdate: str) -> None:
    with open(file_name, 'w') as f:
        f.write(pubdate)


def is_house_update() -> bool:
    house_feed = feedparser.parse(house_rss_url)
    house_channel_pubdate = house_feed.feed.published
    house_last_pubdate = read_pubdate(HOUSE_PUBDATE_FILE_NAME)
    if house_last_pubdate != house_channel_pubdate:
        print(house_last_pubdate, "->", house_channel_pubdate)
        write_pubdate(HOUSE_PUBDATE_FILE_NAME, house_channel_pubdate)
        return True
    return False


def is_senate_update() -> bool:
    senate_feed = feedparser.parse(senate_rss_url)
    senate_channel_pubdate = senate_feed.feed.published
    senate_last_pubdate = read_pubdate(SENATE_PUBDATE_FILE_NAME)
    if senate_last_pubdate != senate_channel_pubdate:
        print(senate_last_pubdate, "->", senate_channel_pubdate)
        write_pubdate(SENATE_PUBDATE_FILE_NAME, senate_channel_pubdate)
        return True
    return False


def fetch_chamber_updates() -> dict[str, bool]:
    house_updated = is_house_update()
    senate_updated = is_senate_update()
    return {
        "house_update": house_updated,
        "senate_update": senate_updated
    }
