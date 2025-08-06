from datetime import datetime
from lib.supabase_client import supabase
from schemas.enums import Chamber, StateCode


def update_db_pubdate(
    state: StateCode,
    chamber: Chamber,
    pubdate: datetime
) -> None:
    print(f"\nUpdating feed pubdate for {state.value} {chamber.value}")
    try:
        supabase \
            .table("feed_pubdates") \
            .upsert(
                {
                    "state": state.value,
                    "chamber": chamber.value,
                    "pubdate": pubdate
                },
                on_conflict="state, chamber"
            ) \
            .execute()
    except Exception as e:
        raise RuntimeError(f"Error updating feed update for {state.value} {chamber.value}: {e}")
