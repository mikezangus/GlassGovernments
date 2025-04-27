from clean_tokens import clean_tokens
from find_universal_tokens import find_universal_tokens
from group_by_type import group_by_type
from tokenize_text import tokenize_text
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PIPELINES_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.append(os.path.dirname(PIPELINES_DIR))
from fetch_from_db import fetch_from_db
from insert_to_db import insert_to_db


def main():
    metadata = fetch_from_db("pa_bill_metadata", { "select": '*' })
    texts = fetch_from_db("pa_bill_texts_flattened", { "select": '*' })
    id_to_text = {}
    for row in texts:
        id_to_text[row["id"]] = row["text"]
    metadata_and_texts = []
    for row in metadata:
        enriched = row.copy()
        enriched["text"] = id_to_text.get(row["id"], "")
        metadata_and_texts.append(enriched)
    metadata_and_tokens = tokenize_text(metadata_and_texts)
    type_to_metadata_and_tokens = group_by_type(metadata_and_tokens)
    cleaned = []
    for type, bills in type_to_metadata_and_tokens.items():
        print(f"\n{type}")
        universal_tokens = find_universal_tokens(bills)
        for bill in bills:
            tokens = clean_tokens(bill, universal_tokens)
            cleaned.append({
                "id": bill["id"],
                "tokens": tokens
            })
    insert_to_db("pa_bill_texts_cleaned", cleaned)
    

if __name__ == "__main__":
    main()
