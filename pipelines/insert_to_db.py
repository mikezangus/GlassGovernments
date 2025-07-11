from supabase_client import supabase
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
    inserted_count = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        print(f"Inserting batch [{i + 1} - {min(i + batch_size, len(rows))}]")
        try:
            table = supabase.table(table_name)
            response = table \
                .upsert(
                    batch,
                    on_conflict=conflict_key,
                    ignore_duplicates=(on_duplicate == OnDuplicate.IGNORE)
                ) \
                .execute()
            inserted_count += len(response.data or [])
        except Exception as e:
            print(f"❌ Error inserting to {table_name}:", e)
    print(f"Inserted {inserted_count} rows to {table_name}")
