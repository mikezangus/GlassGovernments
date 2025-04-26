import os
import re
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from fetch_from_db import fetch_from_db


def tokenize_text(bills: list[dict]) -> list[dict]:
    rows = fetch_from_db("pa_bill_texts_flattened", { "select": '*' })
    id_to_text = { row["id"]: row["text"] for row in rows }
    appended = []
    for row in bills:
        text = id_to_text.get(row["id"], "")
        words = re.findall(r'\b\w+\b', text.lower())
        tokens = set(words)
        enriched_row = row.copy()
        enriched_row["tokens"] = tokens
        appended.append(enriched_row)
    return appended
