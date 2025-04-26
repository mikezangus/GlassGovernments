import feedparser
import os
from parse_guid import parse_guid
from urls import house_rss_url, senate_rss_url


def fetch_guids(url: str) -> list[dict[str, str]]:
    feed = feedparser.parse(url)
    guids = []
    for entry in feed.entries:
        guid = entry.get("guid")
        guids.append(guid)
    return guids


def write_to_csv(guids: list[dict[str, str]], file_name: str) -> None:
    if not guids:
        raise ValueError
    cols = ["year", "session", "bill_type", "bill_num", "print_num"]
    file_exits = os.path.isfile(file_name)
    with open(file_name, 'a', newline="") as f:
        if not file_exits:
            f.write(",".join(cols) + "\n")
        for row in guids:
            line = ",".join(row[field] for field in cols)
            f.write(line + '\n')



def main():
    raw_guids = fetch_guids(house_rss_url)
    guids = []
    for guid in raw_guids:
        parsed_guid = parse_guid(guid)
        guids.append(parsed_guid)
    write_to_csv(guids, "output.csv")
    raw_guids = fetch_guids(senate_rss_url)
    guids = []
    for guid in raw_guids:
        parsed_guid = parse_guid(guid)
        guids.append(parsed_guid)
    write_to_csv(guids, "output.csv")


main()
