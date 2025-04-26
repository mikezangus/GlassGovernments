import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))
from fetch_from_db import fetch_from_db


def main():
    bill_types = fetch_from_db(
        "pa_bill_metadata",
        query_params={ "select": "bill_type" }
    )
    bill_types = list({ row["bill_type"] for row in bill_types })
    ids = {}
    for bill_type in bill_types:
        rows = fetch_from_db(
            "pa_bill_metadata",
            query_params={
                "select": "id",
                "bill_type": f"eq.{bill_type}"
            }
        )
        type_ids = [row["id"] for row in rows]
        ids[bill_type] = type_ids
    


if __name__ == "__main__":
    main()
