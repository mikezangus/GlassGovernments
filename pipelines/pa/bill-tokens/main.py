from clean_tokens import clean_tokens
from find_common_tokens import find_common_tokens
from group_by_type import group_by_type
from tokenize_rows import tokenize_rows
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db
from filter_rows import filter_rows
from insert_to_db import insert_to_db, OnDuplicate


def main():
    flat_rows = fetch_from_db("bill_texts_flat", { "select": '*' })
    if not flat_rows:
        raise ValueError("❌ Failed to fetch from bill_texts_flat")
    existing_tokens_rows = fetch_from_db(
        "bill_tokens",
        { "select": "id" }
    ) or []
    input_rows = filter_rows(flat_rows, existing_tokens_rows, "id")
    raw_tokens_rows = tokenize_rows(input_rows)
    grouped_by_type = group_by_type(raw_tokens_rows)
    output = []
    for type_group in grouped_by_type.values():
        universal_tokens = find_common_tokens(type_group, 0.99)
        for row in type_group:
            output.append({
                "id": row["id"],
                "tokens": clean_tokens(row, universal_tokens)
            })
    insert_to_db("bill_tokens", output, OnDuplicate.MERGE, "id")


if __name__ == "__main__":
    main()
