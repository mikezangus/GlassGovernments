from collections import defaultdict


def find_common_tokens(
    rows: list[dict[str, object]],
    group_name: str,
    threshold: float = 0.99
) -> list[str]:
    if not rows:
        return []
    token_counts = defaultdict(int)
    for row in rows:
        seen_tokens = set(row["raw_tokens"])
        for token in seen_tokens:
            token_counts[token] += 1
    min_count = int(threshold * len(rows))
    common_tokens = []
    for token, count in token_counts.items():
        if count >= min_count:
            common_tokens.append(token)
    print(f"\nCommon tokens for {group_name} group at thresdhold={threshold}\n", common_tokens)
    return common_tokens
