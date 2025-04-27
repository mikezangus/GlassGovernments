def group_by_type(
    bills: list[dict[str, object]]
) -> dict[str, list[dict[str, object]]]:
    grouped = {}
    for bill in bills:
        bill_type = bill["bill_type"]
        if bill_type not in grouped:
            grouped[bill_type] = []
        grouped[bill_type].append(bill)
    return grouped
