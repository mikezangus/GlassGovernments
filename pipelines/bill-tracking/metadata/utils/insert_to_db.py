from dataclasses import asdict, is_dataclass
from shared.lib.supabase_client import supabase
from shared.enums import OnDuplicate


def _serialize_rows(input_rows: list[any]) -> list[dict]:
    output_rows = []
    for input_row in input_rows:
        if is_dataclass(input_row):
            output_row = asdict(input_row)
        elif isinstance(input_row, dict):
            output_row = input_row
        else:
            raise TypeError(f"Unsupported row type: {type(input_row)}")
        output_rows.append(output_row)
    return output_rows


def _deduplicate_rows(rows: list[dict], conflict_key: str) -> list[dict]:
    seen = {}
    for row in rows:
        seen[row[conflict_key]] = row
    return list(seen.values())


def insert_to_db(
    table_name: str,
    rows: list[any],
    on_duplicate: OnDuplicate,
    conflict_key: str | None = None,
    batch_size: int = 500
) -> None:
    print(f"\nInserting {len(rows)} rows to {table_name}")
    if on_duplicate == OnDuplicate.MERGE and not conflict_key:
        raise ValueError("conflict_key must be provided when using OnDuplicate.MERGE")
    rows = _serialize_rows(rows)
    rows = _deduplicate_rows(rows, "id")
    inserted_count = 0
    for i in range(0, len(rows), batch_size):
        batch = rows[i:i + batch_size]
        print(f"Inserting batch [{i + 1} - {min(i + batch_size, len(rows))}]")
        try:
            response = supabase \
                .table(table_name) \
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
