from states.pa.bill_data.run_bill_data import run_bill_data
from states.pa.bill_texts_source.run_bill_texts_source import run_bill_texts_source
from states.pa.fetch_feed_pubdate import fetch_feed_pubdate
from bill_texts_clean.run_bill_texts_clean import run_bill_texts_clean
from bill_tokens.run_bill_tokens import run_bill_tokens
from trigger import trigger
from enums import Chamber


STATE = "PA"


def run_pa():
    trigger_lower = trigger(STATE, Chamber.LOWER, fetch_feed_pubdate)
    trigger_upper = trigger(STATE, Chamber.UPPER, fetch_feed_pubdate)
    if not trigger_lower and not trigger_upper:
        print(f"{STATE} has no updates")
        return
    if trigger_lower:
        run_bill_data(Chamber.LOWER)
    if trigger_upper:
        run_bill_data(Chamber.UPPER)
    run_bill_texts_source()
    run_bill_texts_clean(STATE)
    run_bill_tokens(STATE)


if __name__ == "__main__":
    run_pa()
