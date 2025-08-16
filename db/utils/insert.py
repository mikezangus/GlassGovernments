from dataclasses import asdict, is_dataclass
from db.supabase_config import supabase
from typing import Any, Literal, Sequence


def _serialize_rows(rows: Sequence[any]) -> list[dict]:
    serialized_rows: list[dict] = []
    for row in rows:
        if is_dataclass(row):
            serialized_rows.append(asdict(row))
        elif isinstance(row, dict):
            serialized_rows.append(row)
        else:
            raise TypeError(f"Unsupported row type: {type(row)}")
    return serialized_rows


def _deduplicate_rows(rows: list[dict], conflict_keys: list[str]) -> list[dict]:
    seen: dict[tuple, dict] = {}
    for row in rows:
        key_parts = []
        for conflict_key in conflict_keys:
            key_parts.append(row.get(conflict_key))
        key = tuple(key_parts)
        seen[key] = row
    return list(seen.values())


def insert(
    table_name: str,
    rows: Sequence[Any],
    on_duplicate: Literal["merge", "ignore", "error", None] = None,
    conflict_keys: list[str] | None = None,
    batch_size: int = 1000
) -> None:
    print(f"\nInserting {len(rows)} rows to {table_name}")

    rows = _serialize_rows(rows)

    if on_duplicate == "merge" or on_duplicate == "ignore":
        if not conflict_keys:
            raise ValueError(f"conflict_keys must be provided for on_duplicate={on_duplicate}")
        rows = _deduplicate_rows(rows, conflict_keys)
        on_conflict_str = ','.join(conflict_keys)
        
    affected = 0
    for i in range(0, len(rows), batch_size):
        print(f"Inserting batch [{i + 1} - {min(i + batch_size, len(rows))}]")
        batch = rows[i:i + batch_size]
        query = supabase.table(table_name)
        try:
            if on_duplicate == "merge":
                response = query.upsert(
                    batch,
                    on_conflict=on_conflict_str
                ).execute()
            else:
                response = query.insert(batch).execute()
            affected += len(response.data or [])
        except Exception as e:
            print(f"❌ Error inserting to {table_name}:", e)

    print(f"Inserted {affected} rows to {table_name}")
