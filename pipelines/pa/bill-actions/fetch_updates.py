import feedparser
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(STATE_DIR))
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(os.path.dirname(PIPELINES_DIR))
from fetch_from_db import fetch_from_db


HOUSE_RSS_URL = "https://www.legis.state.pa.us/WU01/LI/RSS/HouseBills.xml"
SENATE_RSS_URL = "https://www.legis.state.pa.us/WU01/LI/RSS/SenateBills.xml"



def parse_metadata(guid: str) -> dict[str, str]:

    guid_len = len(guid)
    i = 0

    year = ""
    while i < 4 and guid[i].isdigit():
        year += guid[i]
        i += 1
    if len(year) == 0:
        raise ValueError

    session = ""
    while i < guid_len and guid[i].isdigit():
        session += guid[i]
        i += 1
    if len(session) == 0:
        raise ValueError

    bill_type = ""
    while i < guid_len and guid[i].isalpha():
        bill_type += guid[i]
        i += 1
    if len(bill_type) == 0:
        raise ValueError

    bill_num = ""
    while i < guid_len and guid[i].isdigit():
        bill_num += guid[i]
        i += 1
    if len(bill_num) == 0:
        raise ValueError

    print_num = ""
    while i < guid_len and guid[i].isalpha():
        i += 1
    while i < guid_len and guid[i].isdigit():
        print_num += guid[i]
        i += 1
    if len(print_num) == 0:
        raise ValueError

    return {
        "guid": guid,
        "year": year,
        "session": session,
        "bill_type": bill_type,
        "bill_num": bill_num,
        "print_num": print_num
    }


def fetch_rss_actions(url: str) -> list[dict[str, str]]:
    feed = feedparser.parse(url)
    actions = []
    for entry in feed.entries:
        guid = entry.get("id")
        try:
            metadata = parse_metadata(guid)
        except:
            continue
        pubdate = entry.get("published")

        actions.append({
            "guid": metadata["guid"],
            "year": metadata["year"],
            "session": metadata["session"],
            "bill_type": metadata["bill_type"],
            "bill_num": metadata["bill_num"],
            "print_num": metadata["print_num"],
            "pubdate": pubdate
        })
    return actions



def fetch_updates() -> list[dict[str, str]]:

    updates = []

    db_actions = fetch_from_db(
        "bill_actions",
        query_params={ "select": "guid, pubdate" }
    )

    db_guid_to_pubdate = {}
    for action in db_actions:
        guid = action["guid"]
        pubdate = action["pubdate"]
        db_guid_to_pubdate[guid] = pubdate

    rss_actions = []
    for url in [HOUSE_RSS_URL, SENATE_RSS_URL]:
        rss_actions.extend(fetch_rss_actions(url))
    
    for action in rss_actions:
        guid = action["guid"]
        rss_pubdate = action["pubdate"]
        if guid not in db_guid_to_pubdate or db_guid_to_pubdate[guid] != rss_pubdate:
            updates.append({
                "guid": guid,
                "year": action["year"],
                "session": action["session"],
                "bill_type": action["bill_type"],
                "bill_num": action["bill_num"],
                "print_num": action["print_num"],
                "pubdate": rss_pubdate
            })

    return updates
