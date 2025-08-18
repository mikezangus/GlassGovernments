from datetime import datetime
from ....db.supabase_config import supabase


def fetch_db_pubdate(state: str, chamber: str) -> datetime | None:
    try:
        response = supabase \
            .table("feed_pubdates") \
            .select("pubdate") \
            .eq("state", state) \
            .eq("chamber", chamber) \
            .maybe_single() \
            .execute()
    except Exception as e:
        raise RuntimeError(f"Error fetching pubdate for {state} {chamber}: {e}")
    if not response or not response.data or not response.data["pubdate"]:
        return None
    return response.data["pubdate"]
