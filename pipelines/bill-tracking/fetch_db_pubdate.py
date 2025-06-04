from datetime import datetime
from chamber_type import Chamber

import os
BILL_TRACKING_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(BILL_TRACKING_DIR)

import sys
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db


def fetch_db_pubdate(state: str, chamber: Chamber) -> datetime | None:
    rows = fetch_from_db(
        "feed_updates",
        {
            "select": "pubdate",
            "state": f"eq.{state.upper()}",
            "chamber": f"eq.{chamber.value}"
        }
    )
    if not rows:
        return None
    return rows[0]["pubdate"]
