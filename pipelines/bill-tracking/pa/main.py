import os
PA_DIR = os.path.dirname(os.path.abspath(__file__))
BILL_TRACKING_DIR = os.path.dirname(PA_DIR)
BILL_DATA_DIR = os.path.join(PA_DIR, "bill-data")
BILL_TEXTS_SOURCE_DIR = os.path.join(PA_DIR, "bill-texts-source")
BILL_TRACKING_DIR = os.path.dirname(PA_DIR)
BILL_TEXTS_CLEAN_DIR = os.path.join(BILL_TRACKING_DIR, "bill-texts-clean")
BILL_TOKENS_DIR = os.path.join(BILL_TRACKING_DIR, "bill-tokens")
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)

from fetch_feed_pubdate import fetch_feed_pubdate

import sys
sys.path.append(BILL_TRACKING_DIR)
from trigger import trigger
sys.path.append(BILL_DATA_DIR)
print(BILL_DATA_DIR)


sys.path.append(PIPELINES_DIR)
from enums import Chamber


STATE = "PA"


def main():
    trigger_lower = trigger(STATE, Chamber.LOWER, fetch_feed_pubdate)
    trigger_upper = trigger(STATE, Chamber.UPPER, fetch_feed_pubdate)
    if not trigger_lower and not trigger_upper:
        print(f"{STATE} has no updates")
        return
    if trigger_lower:
        print("lower trigger hit")
    #     process_bill_data(Chamber.LOWER)
    if trigger_upper:
        print("upper trigger hit")
    #     process_bill_data(Chamber.UPPER)
    # process_bill_texts_source()
    # process_bill_texts_clean(STATE)
    # process_bill_tokens(STATE)


if __name__ == "__main__":
    main()
