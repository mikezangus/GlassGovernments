from datetime import datetime
from ...shared.enums import Chamber
from typing import Callable
from .fetch_db_pubdate import fetch_db_pubdate
from .update_db_pubdate import update_db_pubdate


def trigger(
    state: str,
    chamber: Chamber,
    fn_fetch_state_feed_pubdate: Callable[[Chamber], datetime]
) -> bool:
    db_pubdate = fetch_db_pubdate(state, chamber.value)
    feed_pubdate = fn_fetch_state_feed_pubdate(chamber)
    if db_pubdate is None or feed_pubdate > db_pubdate:
        update_db_pubdate(state, chamber.value, feed_pubdate)
        return True
    return False
