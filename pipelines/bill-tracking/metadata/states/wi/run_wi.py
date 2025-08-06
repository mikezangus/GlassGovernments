import feedparser

import json


url = "https://docs.legis.wisconsin.gov/feed/custom/allfloor"
feed = feedparser.parse(url)
with open("wi_feed.json", 'w', encoding='utf-8') as f:
        json.dump(feed.entries, f, indent=2, ensure_ascii=False)
print(feed)