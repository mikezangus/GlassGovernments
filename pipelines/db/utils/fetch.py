from ..supabase_config import supabase


def fetch(
    table_name: str,
    query_params: dict = None,
    select: str = '*',
    batch_size: int = 1000
) -> list[dict]:
    rows: list[dict] = []
    offset = 0
    while True:
        query = supabase.table(table_name).select(select)
        if query_params:
            for key, value in query_params.items():
                query = query.eq(key, value)
        query = query.range(offset, offset + batch_size)
        try:
            response = query.execute()
            batch_rows = response.data or []
            rows.extend(batch_rows)
            if len(batch_rows) < batch_size:
                break
            offset += batch_size
        except Exception as e:
            print(f"❌ Error fetching from {table_name}: {e}")
            break
    return rows
