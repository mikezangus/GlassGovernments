from datetime import datetime
from typing import Callable
from schemas.enums import Chamber
from utils.fetch_db_pubdate import fetch_db_pubdate
from utils.update_db_pubdate import update_db_pubdate


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
