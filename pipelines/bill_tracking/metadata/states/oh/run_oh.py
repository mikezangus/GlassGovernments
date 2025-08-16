from shared.enums import OnDuplicate, StateCode
from shared.rows import BillMetadataRow
from shared.utils.insert_to_db import insert_to_db
from shared.utils.get_html import get_html
from metadata.states.oh.fetch_raw_metadata import fetch_raw_metadata
from metadata.states.oh.parse_metadata_row import parse_metadata_row


SESSION = 136


def run_oh() -> None:
    state = StateCode.OH
    print(f"\n\nRunning bill metadata for {state.value}")

    url = f"https://statusreport.lsc.ohio.gov/legislation/{SESSION}?type=All&sort=Name"
    html = get_html(url)
    raw_metadata_rows = fetch_raw_metadata(html)

    metadata_rows: list[BillMetadataRow] = []
    for raw_metadata_row in raw_metadata_rows:
        metadata_rows.append(parse_metadata_row(
            raw_metadata_row,
            SESSION,
            state.value
        ))

    insert_to_db("bill_metadata", metadata_rows, OnDuplicate.MERGE, ["id"])
