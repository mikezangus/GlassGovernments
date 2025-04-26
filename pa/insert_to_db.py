import requests
from db import supabase_headers, supabase_url


def insert_to_db(table_name: str, data: list[dict]) -> None:
    url = f"{supabase_url}/rest/v1/{table_name}"
    response = requests.post(url, headers=supabase_headers, json=data)
    if response.ok:
        inserted = response.json()
        print(f"Inserted {len(inserted)} rows to {table_name}")
    else:
        print(f"Error inserting to {table_name}:", response.status_code, response.text)
