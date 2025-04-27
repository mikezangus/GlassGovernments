import re


def tokenize_text(bills: list[dict[str, object]]) -> list[dict[str, object]]:
    tokenized = []
    for bill in bills:
        text = bill["text"]
        tokens = re.findall(r'\b\w+\b', text.lower())
        enriched = bill.copy()
        enriched["raw_tokens"] = tokens
        tokenized.append(enriched)
    return tokenized
