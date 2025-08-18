from datetime import datetime
from ....db.supabase_config import supabase


def update_db_pubdate(
    state: str,
    chamber: str,
    pubdate: datetime
) -> None:
    print(f"\nUpdating feed pubdate for {state} {chamber}")
    try:
        supabase \
            .table("feed_pubdates") \
            .upsert(
                {
                    "state": state,
                    "chamber": chamber,
                    "pubdate": pubdate
                },
                on_conflict="state, chamber"
            ) \
            .execute()
    except Exception as e:
        raise RuntimeError(f"Error updating feed update for {state} {chamber}: {e}")
