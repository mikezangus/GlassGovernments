import os
PA_DIR = os.path.dirname(os.path.abspath(__file__))
BILL_DATA_DIR = os.path.join(PA_DIR, "bill-data")
BILL_TEXTS_SOURCE_DIR = os.path.join(PA_DIR, "bill-texts-source")
BILL_TRACKING_DIR = os.path.dirname(PA_DIR)
BILL_TEXTS_CLEAN_DIR = os.path.join(BILL_TRACKING_DIR, "bill-texts-clean")
BILL_TOKENS_DIR = os.path.join(BILL_TRACKING_DIR, "bill-tokens")
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)

import sys
sys.path.append(PA_DIR)
from fetch_feed_pubdate import fetch_feed_pubdate
sys.path.append(BILL_DATA_DIR)
from process_bill_data import process_bill_data
sys.path.append(BILL_TEXTS_SOURCE_DIR)
from process_bill_texts_source import process_bill_texts_source
sys.path.append(BILL_TRACKING_DIR)
from fetch_db_pubdate import fetch_db_pubdate
sys.path.append(BILL_TEXTS_CLEAN_DIR)
from process_bill_texts_clean import process_bill_texts_clean
sys.path.append(BILL_TOKENS_DIR)
from process_bill_tokens import process_bill_tokens
sys.path.append(PIPELINES_DIR)
from chamber_type import Chamber
from insert_to_db import insert_to_db, OnDuplicate


STATE = "PA"


def main():
    lower_db_pubdate = fetch_db_pubdate(STATE, Chamber.LOWER)
    lower_feed_pubdate = fetch_feed_pubdate(Chamber.LOWER)
    upper_db_pubdate = fetch_db_pubdate(STATE, Chamber.UPPER)
    upper_feed_pubdate = fetch_feed_pubdate(Chamber.UPPER)
    updated = False
    if not lower_db_pubdate or lower_feed_pubdate > lower_db_pubdate:
        process_bill_data(Chamber.LOWER)
        insert_to_db(
            "feed_updates",
            [{
                "chamber": Chamber.LOWER.value,
                "state": STATE,
                "pubdate": lower_feed_pubdate
            }],
            OnDuplicate.MERGE,
            "chamber, state"
        )
        updated = True
    if not upper_db_pubdate or upper_feed_pubdate > upper_db_pubdate:
        process_bill_data(Chamber.UPPER)
        insert_to_db(
            "feed_updates",
            [{
                "chamber": Chamber.UPPER.value,
                "state": STATE,
                "pubdate": upper_feed_pubdate
            }],
            OnDuplicate.MERGE,
            "chamber, state"
        )
        updated = True
    if not updated:
        print("No updates")
        return
    process_bill_texts_source()
    process_bill_texts_clean(STATE)
    process_bill_tokens(STATE)


if __name__ == "__main__":
    main()
