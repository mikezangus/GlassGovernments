from bill_tokens.clean_tokens import clean_tokens
from bill_tokens.find_common_tokens import find_common_tokens
from bill_tokens.group_by_type import group_by_type
from bill_tokens.tokenize_rows import tokenize_rows
from fetch_from_db import fetch_from_db
from insert_to_db import insert_to_db, OnDuplicate


def run_bill_tokens(state: str) -> None:
    print("\n\nProcessing bill tokens")
    input_rows = fetch_from_db(
        "bill_texts_clean",
        { "state": state.upper() }
    )
    if not input_rows:
        raise ValueError("❌ Failed to fetch from bill_texts_clean")
    tokens_rows = tokenize_rows(input_rows)
    grouped_by_type = group_by_type(tokens_rows)
    output = []
    for group_name, group_rows in grouped_by_type.items():
        common_tokens = find_common_tokens(group_rows, group_name, 0.75)
        for row in group_rows:
            output.append({
                "bill_id": row["bill_id"],
                "state": state.upper(),
                "tokens": clean_tokens(row, common_tokens)
            })
    insert_to_db("bill_tokens", output, OnDuplicate.MERGE, "bill_id")
