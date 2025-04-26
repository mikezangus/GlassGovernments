from collections import Counter


THRESHOLD = 0.99


def find_common_tokens(bills: list[dict]) -> list[str]:
    all_tokens = []
    for bill in bills:
        tokens = bill["tokens"]
        all_tokens.extend(tokens)
    counter = Counter(all_tokens)
    if not counter:
        return []
    sorted_counts = sorted(counter.values(), reverse=True)
    threshold_index = int(len(sorted_counts) * (1 - THRESHOLD))
    if threshold_index >= len(sorted_counts):
        threshold_index = len(sorted_counts) - 1
    threshold = sorted_counts[threshold_index]
    common_tokens = [word for word, count in counter.items() if count >= threshold]
    return common_tokens
