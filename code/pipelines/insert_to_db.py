import requests
from supabase_config import supabase_headers, supabase_api_url
from enum import Enum


class OnDuplicate(Enum):
    IGNORE = "ignore"
    MERGE = "merge"


def insert_to_db(
    table_name: str,
    rows: list[dict],
    on_duplicate: OnDuplicate,
    conflict_key: str | None = None,
    batch_size: int = 500
) -> None:
    print(f"\nInserting {len(rows)} rows to {table_name}")
    if on_duplicate == OnDuplicate.MERGE and not conflict_key:
        raise ValueError("conflict_key must be provided when using OnDuplicate.MERGE")
    url = f"{supabase_api_url}/rest/v1/{table_name}"
    if conflict_key:
        url += f"?on_conflict={conflict_key}"
    headers = {
        **supabase_headers,
        "Prefer": f"resolution={on_duplicate.value}-duplicates,return=representation"
    }
    inserted_count = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        print(f"Inserting batch [{i + 1} - {min(i + batch_size, len(rows))}]")
        try:
            response = requests.post(url, headers=headers, json=batch)
        except Exception as e:
            print("Error:", e)
        if response.ok:
            inserted = response.json()
            inserted_count += len(inserted)
        else:
            print(f"❌ Error inserting to {table_name}:", response.status_code, response.text)
    print(f"Inserted {inserted_count} rows to {table_name}")
