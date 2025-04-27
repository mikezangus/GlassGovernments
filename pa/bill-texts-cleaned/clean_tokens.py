def clean_tokens(
    bill: dict[str, object], universal_tokens: set[str]
) -> list[str]:
    bad_words = set(universal_tokens)
    id = bill["id"].lower()
    bad_words.add(id)
    bad_words.add(id.replace("p", "pn", 1))
    bad_words.add(str(bill["bill_num"]))
    bad_words.add(str(bill["print_num"]))
    cleaned_tokens = []
    for token in bill["raw_tokens"]:
        if token not in bad_words:
            cleaned_tokens.append(token)
    return cleaned_tokens
