def clean_tokens(
    row: dict[str, object],
    common_tokens: set[str]
) -> list[str]:
    bad_words = set(common_tokens)
    _, year, session, bill_type, bill_num, print_num = row["id"] \
        .lower() \
        .split('_')
    bad_words.add(year)
    bad_words.add(bill_num)
    bad_words.add(print_num)
    bad_words.add(f"{year}{session}{bill_type}{bill_num}p{print_num}")
    bad_words.add(f"{year}{session}{bill_type}{bill_num}pn{print_num}")
    cleaned_tokens = []
    for token in row["raw_tokens"]:
        if token not in bad_words:
            cleaned_tokens.append(token)
    return cleaned_tokens
