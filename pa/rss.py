import feedparser


BASE_URL = "https://legis.state.pa.us/"
RSS_URL = BASE_URL + "WU01/LI/RSS/"
HOUSE_URL = RSS_URL+ "HouseBills.xml"
SENATE_URL = RSS_URL + "SenateBills.xml"
HOUSE_PUBDATE_FILE_NAME = "last_pubdate_house.txt"
SENATE_PUBDATE_FILE_NAME = "last_pubdate_senate.txt"


house_feed = feedparser.parse(HOUSE_URL)
house_channel_pubdate = house_feed.feed.published


senate_feed = feedparser.parse(SENATE_URL)
senate_channel_pubdate = senate_feed.feed.published


def read_pubdate(file_name: str) -> str:
    with open(file_name, 'r') as f:
        return f.read().strip()


def write_pubdate(file_name: str, pubdate: str) -> None:
    with open(file_name, 'w') as f:
        f.write(pubdate)


house_last_pubdate = read_pubdate(HOUSE_PUBDATE_FILE_NAME)
if house_last_pubdate != house_channel_pubdate:
    print(house_last_pubdate, "->", house_channel_pubdate)
    write_pubdate(HOUSE_PUBDATE_FILE_NAME, house_channel_pubdate)


senate_last_pubdate = read_pubdate(SENATE_PUBDATE_FILE_NAME)
if senate_last_pubdate != senate_channel_pubdate:
    print(senate_last_pubdate, "->", senate_channel_pubdate)
    write_pubdate(SENATE_PUBDATE_FILE_NAME, senate_channel_pubdate)

