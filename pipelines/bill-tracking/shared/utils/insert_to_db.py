from dataclasses import asdict, is_dataclass
from shared.enums import OnDuplicate
from shared.lib.supabase_client import supabase


def _serialize_rows(rows: list[any]) -> list[dict]:
    output_rows = []
    for row in rows:
        if is_dataclass(row):
            output_rows.append(asdict(row))
        elif isinstance(row, dict):
            output_rows.append(row)
        else:
            raise TypeError(f"Unsupported row type: {type(row)}")
    return output_rows


def _normalize_none_to_empty(rows: list[dict], conflict_keys: list[str] | None = None) -> None:
    for row in rows:
        if conflict_keys is None:
            for key, value in row.items():
                if value is None:
                    row[key] = ''
                elif isinstance(value, str) and value.strip() == '':
                    row[key] = ''
        else:
            for conflict_key in conflict_keys:
                value = row.get(conflict_key)
                if value is None:
                    row[conflict_key] = ''
                elif isinstance(value, str) and value.strip() == '':
                    row[conflict_key] = ''


def _deduplicate_rows(rows: list[dict], conflict_keys: list[str]) -> list[dict]:
    seen: dict[tuple, dict] = {}
    for row in rows:
        key_parts = []
        for conflict_key in conflict_keys:
            key_parts.append(row.get(conflict_key))
        key = tuple(key_parts)
        seen[key] = row
    return list(seen.values())


def insert_to_db(
    table_name: str,
    rows: list[any],
    on_duplicate: OnDuplicate,
    conflict_keys: list[str] | None = None,
    batch_size: int = 500
) -> None:
    print(f"\nInserting {len(rows)} rows to {table_name}")

    rows = _serialize_rows(rows)
    _normalize_none_to_empty(rows, conflict_keys)

    if on_duplicate == OnDuplicate.MERGE or on_duplicate == OnDuplicate.IGNORE:
        if not conflict_keys:
            raise ValueError(f"conflict_keys must be provided for on_duplicate={on_duplicate}")
        rows = _deduplicate_rows(rows, conflict_keys)
        on_conflict_str = ",".join(conflict_keys)
    else:
        on_conflict_str = None
        
    affected = 0
    for i in range(0, len(rows), batch_size):
        print(f"Inserting batch [{i + 1} - {min(i + batch_size, len(rows))}]")
        batch = rows[i:i + batch_size]
        query = supabase.table(table_name)
        try:
            if on_duplicate == OnDuplicate.MERGE:
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
