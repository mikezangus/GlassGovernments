import os
import sys
from tokenize_text import tokenize_text
from find_common_tokens import find_common_tokens
from group_by_type import group_by_type
from fetch_bill_metadata import fetch_bill_metadata
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from insert_to_db import insert_to_db


def main():
    bill_metadata = fetch_bill_metadata()
    tokenized = tokenize_text(bill_metadata)
    grouped_by_type = group_by_type(tokenized)
    cleaned = []
    for _, bills in grouped_by_type.items():
        common_words = find_common_tokens(bills)
        for bill in bills:
            uncommon_words = bill["tokens"] - set(common_words)
            uncommon_words.discard(bill["id"].lower())
            uncommon_words.discard(str(bill["bill_num"]))
            uncommon_words.discard(str(bill["print_num"]))
            cleaned.append({
                "id": bill["id"],
                "tokens": list(uncommon_words)
            })
    insert_to_db("pa_bill_texts_cleaned", cleaned)
    

if __name__ == "__main__":
    main()
