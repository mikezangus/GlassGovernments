from datetime import datetime
from enums import Chamber, StateCode
from supabase_client import supabase


def update_db_pubdate(
    state: StateCode,
    chamber: Chamber,
    pubdate: datetime
) -> None:
    print(f"Updating feed pubdate for {state} {chamber.value}")
    try:
        supabase \
            .table("feed_pubdates") \
            .upsert(
                {
                    "state": state,
                    "chamber": chamber.value,
                    "pubdate": pubdate
                },
                on_conflict="state, chamber"
            ) \
            .execute()
    except Exception as e:
        raise RuntimeError(f"Error updating feed update for {state} {chamber.value}: {e}")
