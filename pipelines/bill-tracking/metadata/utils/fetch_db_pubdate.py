from datetime import datetime
from lib.supabase_client import supabase
from schemas.enums import Chamber


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
