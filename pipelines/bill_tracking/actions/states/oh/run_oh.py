from .extract_raw_actions import extract_raw_actions
from ....shared.enums import OnDuplicate
from ....shared.rows import BillActionsRow
from ....shared.utils.get_html import get_html
from .....db.utils.fetch import fetch
from .....db.utils.insert import insert



INSERT_BATCH_SIZE = 100


def run_oh() -> None:
    metadata_rows =  fetch(
        "bill_metadata",
        { "state": "OH" },
        "id, state, bill_url"
    )
    for i, metadata_row in enumerate(metadata_rows):
        # url = metadata_row.get("bill_url")
        url = "https://statusreport.lsc.ohio.gov/legislation/view/136?type=SB&number=1"
        print(f"{i + 1}/{len(metadata_rows)} | {url}")
        if not url:
            continue
        html = get_html(url)
        raw_actions = extract_raw_actions(html)
        
        for chamber, actions in raw_actions.items():
            print(f"\n=== {chamber.upper()} ===")
            for key, value in actions.items():
                print(f"{key}: {value}")

        return
    return
