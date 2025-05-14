def clean_tokens(
    row: dict[str, object],
    universal_tokens: set[str]
) -> list[str]:
    bad_words = set(universal_tokens)
    id = row["id"].lower()
    bad_words.add(id)
    bad_words.add(id.replace("p", "pn", 1))
    bill_num, print_num = id.split('_')[4:6]
    bad_words.add(bill_num)
    bad_words.add(print_num)
    cleaned_tokens = []
    for token in row["raw_tokens"]:
        if token not in bad_words:
            cleaned_tokens.append(token)
    return cleaned_tokens
