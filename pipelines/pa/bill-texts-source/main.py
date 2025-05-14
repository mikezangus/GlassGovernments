from fetch_html_from_web import fetch_html_from_web
from extract_text_from_html import extract_text_from_html
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(PIPELINES_DIR)
from fetch_from_db import fetch_from_db
from filter_rows import filter_rows
from insert_to_db import insert_to_db, OnDuplicate


def main():
    metadata_rows = fetch_from_db(
        "bill_metadata",
        query_params={
            "select": "id,text_url",
            "state": "eq.PA"
        }
    )
    if not metadata_rows:
        print("❌ Failed to fetch from bill_metadata")
    existing_text_rows  = fetch_from_db(
        "bill_texts_source",
        query_params={ "select": "id" }
    ) or []
    input_rows = filter_rows(metadata_rows, existing_text_rows, "id")
    output_rows = []
    for (i, input_row) in enumerate(input_rows):
        print(f"[{i + 1}/{len(input_rows)}]", input_row["id"])
        try:
            html = fetch_html_from_web(input_row["text_url"])
        except:
            print("❌ Failed to fetch HTML")
            continue
        output_rows.append({
            "id": input_row["id"],
            "text": extract_text_from_html(html)
        })
    insert_to_db("bill_texts_source", output_rows, OnDuplicate.MERGE, "id")


if __name__ == "__main__":
    main()
