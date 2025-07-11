from datetime import datetime
from typing import Callable
from enums import Chamber
from update_db_pubdate import update_db_pubdate

import os
BILL_TRACKING_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)

import sys
sys.path.append(PIPELINES_DIR)
from supabase_client import supabase


def fetch_db_pubdate(state: str, chamber: Chamber) -> datetime | None:
    try:
        response = supabase \
            .table("feed_pubdates") \
            .select("pubdate") \
            .eq("state", state) \
            .eq("chamber", chamber.value) \
            .maybe_single() \
            .execute()
    except Exception as e:
        raise RuntimeError(f"Error fetching pubdate for {state} {chamber.value}: {e}")
    if not response or not response.data or not response.data["pubdate"]:
        return None
    return response.data["pubdate"]


def trigger(
    state: str,
    chamber: Chamber,
    fetch_state_feed_pubdate: Callable[[Chamber], datetime]
) -> bool:
    db_pubdate = fetch_db_pubdate(state, chamber)
    feed_pubdate = fetch_state_feed_pubdate(chamber)
    if db_pubdate is None or feed_pubdate > db_pubdate:
        update_db_pubdate(state, chamber, feed_pubdate)
        return True
    return False
