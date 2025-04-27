def find_universal_tokens(bills: list[dict[str, object]]) -> list[str]:
    token_sets = []
    for bill in bills:
        token_sets.append(set(bill["raw_tokens"]))
    common_tokens = set.intersection(*token_sets)
    return list(common_tokens)
