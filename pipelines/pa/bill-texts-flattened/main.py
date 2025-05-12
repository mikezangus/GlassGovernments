from flatten_text import flatten_text
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db
from insert_to_db import insert_to_db


def main():
    rows = fetch_from_db(
        "bill_texts_source",
        query_params={"select": '*'}
    )
    flattened_rows = []
    for row in rows:
        flattened_rows.append({
            "id": row["id"],
            "text": flatten_text(row["text"])
        })
    insert_to_db("bill_texts_flat", flattened_rows)


if __name__ == "__main__":
    main()
