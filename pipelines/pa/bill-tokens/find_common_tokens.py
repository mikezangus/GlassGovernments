from collections import defaultdict


def find_common_tokens(
    rows: list[dict[str, object]],
    threshold: float
) -> list[str]:
    if not rows:
        return []
    token_counts = defaultdict(int)
    row_count = len(rows)
    for row in rows:
        seen_tokens = set(row["raw_tokens"])
        for token in seen_tokens:
            token_counts[token] += 1
    min_count = int(threshold * row_count)
    common_tokens = [
        token for token, count in token_counts.items()
        if count >= min_count
    ]
    return common_tokens
