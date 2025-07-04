import feedparser




url = "https://docs.legis.wisconsin.gov/feed/custom/allfloor"
feed = feedparser.parse(url)
print(feed)