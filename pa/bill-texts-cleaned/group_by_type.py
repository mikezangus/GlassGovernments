def group_by_type(bills: list[dict]) -> dict[str, list[dict]]:
    split = {}
    for bill in bills:
        bill_type = bill["bill_type"]
        if bill_type not in split:
            split[bill_type] = []
        split[bill_type].append(bill)
    return split
