from datetime import datetime
from enums import Chamber, StateCode

import os
BILL_TRACKING_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)

import sys
sys.path.append(PIPELINES_DIR)
from supabase_client import supabase


def update_db_pubdate(
    state: StateCode,
    chamber: Chamber,
    pubdate: datetime
) -> None:
    print("state:", state)
    print("chamber value:", chamber.value)
    print("pubdate:", pubdate)
    try:
        supabase \
            .table("feed_pubdates") \
            .update({ "pubdate": pubdate }) \
            .match({ "state": state, "chamber": chamber.value }) \
            .execute()
    except Exception as e:
        raise RuntimeError(f"Error updating feed update for {state} {chamber.value}: {e}")
