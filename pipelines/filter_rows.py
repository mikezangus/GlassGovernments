def filter_rows(
    base_rows: list[dict],
    filter_rows: list[dict] | None,
    filter_col: str
) -> list[dict]:
    if not filter_rows:
        return base_rows
    existing_rows = set()
    for row in filter_rows:
        existing_rows.add(row[filter_col])
    filtered_rows = []
    for row in base_rows:
        if row[filter_col] not in existing_rows:
            filtered_rows.append(row)
    return filtered_rows
