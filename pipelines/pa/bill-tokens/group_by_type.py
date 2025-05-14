def group_by_type(
    rows: list[dict[str, object]]
) -> dict[str, list[dict[str, object]]]:
    grouped = {}
    for row in rows:
        bill_type = row["id"].split('_')[3]
        if bill_type not in grouped:
            grouped[bill_type] = []
        grouped[bill_type].append(row)
    return grouped
