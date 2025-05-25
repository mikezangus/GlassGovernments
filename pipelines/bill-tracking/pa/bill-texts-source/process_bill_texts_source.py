from fetch_html_from_web import fetch_html_from_web
from extract_text_from_html import extract_text_from_html

import os
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
PIPELINES_DIR = os.path.dirname(STATE_DIR)

import sys
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db
from filter_rows import filter_rows
from insert_to_db import insert_to_db, OnDuplicate


def process_bill_texts_source() -> None:
    print("\n\nProcessing bill texts source")
    metadata_rows = fetch_from_db(
        "bill_metadata",
        {
            "select": "bill_id,text_url",
            "state": "eq.PA"
        }
    )
    if not metadata_rows:
        raise ValueError("❌ Failed to fetch from bill_metadata")
    existing_text_rows  = fetch_from_db(
        "bill_texts_source",
        { "select": "bill_id" }
    ) or []
    input_rows = filter_rows(metadata_rows, existing_text_rows, "bill_id")
    output_rows = []
    for (i, input_row) in enumerate(input_rows):
        print(f"[{i + 1}/{len(input_rows)}]", input_row["bill_id"])
        try:
            html = fetch_html_from_web(input_row["text_url"])
        except:
            print("❌ Failed to fetch HTML")
            continue
        output_rows.append({
            "bill_id": input_row["bill_id"],
            "state": "PA",
            "text": extract_text_from_html(html)
        })
    insert_to_db("bill_texts_source", output_rows, OnDuplicate.MERGE, "bill_id")
