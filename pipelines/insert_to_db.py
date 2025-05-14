import requests
from db import supabase_headers, supabase_url
from enum import Enum


class OnDuplicate(Enum):
    IGNORE = "ignore"
    MERGE = "merge"


def insert_to_db(
    table_name: str,
    data: list[dict],
    on_duplicate: OnDuplicate,
    conflict_key: str | None = None
) -> None:
    print(f"\nInserting to {table_name}")
    if on_duplicate == OnDuplicate.MERGE and not conflict_key:
        raise ValueError("conflict_key must be provided when using OnDuplicate.MERGE")
    url = f"{supabase_url}/rest/v1/{table_name}"
    if conflict_key:
        url += f"?on_conflict={conflict_key}"
    headers = {
        **supabase_headers,
        "Prefer": f"resolution={on_duplicate.value}-duplicates,return=representation"
    }
    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        inserted = response.json()
        print(f"Inserted {len(inserted)} rows to {table_name}")
    else:
        print(f"Error inserting to {table_name}:", response.status_code, response.text)
