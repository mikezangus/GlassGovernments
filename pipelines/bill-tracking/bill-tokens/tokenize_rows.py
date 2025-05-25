import re


def tokenize_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    tokenized = []
    for row in rows:
        text = row["text"]
        tokens = re.findall(r'\b\w+\b', text.lower())
        tokenized.append({ "bill_id": row["bill_id"], "raw_tokens": tokens })
    return tokenized
