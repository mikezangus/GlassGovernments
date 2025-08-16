from bill_texts_clean.flatten_text import flatten_text
from bill_texts_clean.remove_heading import remove_heading
from fetch_from_db import fetch_from_db
from filter_rows import filter_rows
from insert_to_db import insert_to_db, OnDuplicate


def run_bill_texts_clean(state: str) -> None:
    print("\n\nProcessing bill texts clean")
    source_rows = fetch_from_db(
        "bill_texts_source",
        { "state": state.upper() }
    )
    if not source_rows:
        raise ValueError("❌ Failed to fetch from bill_texts_source")
    existing_clean_rows = fetch_from_db(
        "bill_texts_clean",
        { "state": state.upper() }
    )
    input_rows = filter_rows(source_rows, existing_clean_rows, "bill_id")
    output_rows = []
    for row in input_rows:
        headerless_text = remove_heading(row["text"])
        output_rows.append({
            "bill_id": row["bill_id"],
            "state": state.upper(),
            "text": flatten_text(headerless_text)
        })
    insert_to_db("bill_texts_clean", output_rows, OnDuplicate.MERGE, "bill_id")
