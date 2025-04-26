import requests
from db import supabase_headers, supabase_url


def fetch_from_db(table_name: str, query_params: dict = None) -> list[dict]:
    url = f"{supabase_url}/rest/v1/{table_name}"
    response = requests.get(url, headers=supabase_headers, params=query_params or {})
    if response.ok:
        return response.json()
    else:
        print(f"Error fetching from {table_name}:", response.status_code, response.text)
        return []
