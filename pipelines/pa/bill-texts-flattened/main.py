from flatten_text import flatten_text
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db
from filter_rows import filter_rows
from insert_to_db import insert_to_db, OnDuplicate


def main():
    source_rows = fetch_from_db("bill_texts_source", { "select": '*' })
    if not source_rows:
        raise ValueError("❌ Failed to fetch from bill_texts_source")
    existing_flat_rows = fetch_from_db("bill_texts_flat", { "select": "id" })
    input_rows = filter_rows(source_rows, existing_flat_rows, "id")
    output_rows = []
    for row in input_rows:
        output_rows.append({
            "id": row["id"],
            "text": flatten_text(row["text"])
        })
    insert_to_db("bill_texts_flat", output_rows, OnDuplicate.MERGE, "id")


if __name__ == "__main__":
    main()
