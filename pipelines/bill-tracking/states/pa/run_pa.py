import os
PA_DIR = os.path.dirname(os.path.abspath(__file__))
STATES_DIR = os.path.dirname(PA_DIR)
BILL_TRACKING_DIR = os.path.dirname(STATES_DIR)
BILL_DATA_DIR = os.path.join(PA_DIR, "bill-data")
BILL_TEXTS_SOURCE_DIR = os.path.join(PA_DIR, "bill-texts-source")
BILL_TEXTS_CLEAN_DIR = os.path.join(BILL_TRACKING_DIR, "bill-texts-clean")
BILL_TOKENS_DIR = os.path.join(BILL_TRACKING_DIR, "bill-tokens")
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)
import sys
sys.path.append(PA_DIR)
from fetch_feed_pubdate import fetch_feed_pubdate
sys.path.append(BILL_TRACKING_DIR)
from trigger import trigger
sys.path.append(BILL_DATA_DIR)
from run_bill_data import run_bill_data
sys.path.append(BILL_TEXTS_SOURCE_DIR)
from run_bill_texts_source import run_bill_texts_source
sys.path.append(BILL_TEXTS_CLEAN_DIR)
from run_bill_texts_clean import run_bill_texts_clean
sys.path.append(BILL_TOKENS_DIR)
from run_bill_tokens import run_bill_tokens
sys.path.append(PIPELINES_DIR)
from enums import Chamber


STATE = "PA"


def run_pa():
    trigger_lower = trigger(STATE, Chamber.LOWER, fetch_feed_pubdate)
    trigger_upper = trigger(STATE, Chamber.UPPER, fetch_feed_pubdate)
    if not trigger_lower and not trigger_upper:
        print(f"{STATE} has no updates")
        return
    if trigger_lower:
        print("lower trigger hit")
        run_bill_data(Chamber.LOWER)
    if trigger_upper:
        print("upper trigger hit")
        run_bill_data(Chamber.UPPER)
    run_bill_texts_source()
    run_bill_texts_clean(STATE)
    run_bill_tokens(STATE)


if __name__ == "__main__":
    run_pa()
