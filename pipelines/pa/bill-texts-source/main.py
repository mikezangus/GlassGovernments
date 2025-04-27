from fetch_html_from_web import fetch_html_from_web
from extract_text_from_html import extract_text_from_html
import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.dirname(CURRENT_DIR)
sys.path.append(os.path.dirname(STATE_DIR))
from urls import bill_text_url
PIPELINES_DIR = os.path.dirname(STATE_DIR)
sys.path.append(os.path.dirname(PIPELINES_DIR))
from fetch_from_db import fetch_from_db
from insert_to_db import insert_to_db


def main():
    rows = fetch_from_db("pa_bill_metadata", query_params={ "select": '*' })
    texts = []
    for (i, row) in enumerate(rows):
        print(f"[{i + 1}/{len(rows)}]", row["id"])
        try:
            html = fetch_html_from_web(
                bill_text_url(
                    row["year"],
                    row["session"],
                    row["bill_type"],
                    row["bill_num"],
                    row["print_num"]
                )
            )
        except:
            print('❌ Failed to fetch HTML')
            continue
        text = extract_text_from_html(html)
        texts.append({
            "id": row["id"],
            "text": text
        })
    insert_to_db("pa_bill_texts_source", texts)


if __name__ == "__main__":
    main()
