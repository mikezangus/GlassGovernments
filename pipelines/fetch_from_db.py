import requests
from pipelines.db import supabase_headers, supabase_url


def fetch_from_db(table_name: str, query_params: dict = None) -> list[dict]:
    url = f"{supabase_url}/rest/v1/{table_name}"
    rows = []
    limit = 1000
    offset = 0
    while True:
        headers = supabase_headers.copy()
        headers["Range-Unit"] = "items"
        headers["Range"] = f"{offset}-{offset + limit - 1}"
        response = requests.get(url, headers=headers, params=query_params or {})
        if not response.ok:
            print(f"Error fetching from {table_name}:", response.status_code, response.text)
            break
        batch_rows = response.json()
        rows.extend(batch_rows)
        if len(batch_rows) < limit:
            break
        offset += limit
    return rows
