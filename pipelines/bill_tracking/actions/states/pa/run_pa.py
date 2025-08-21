from .parse_events import parse_actions
from ...utils.get_action import get_action
from ....shared.enums import OnDuplicate
from ....shared.rows import BillActionsRow
from ....shared.utils.get_html import get_html
from .....db.utils.fetch import fetch
from .....db.utils.insert import insert


INSERT_BATCH_SIZE = 100


def run_pa() -> None:
    actions_rows: BillActionsRow = []
    bill_rows = fetch(
        "bill_metadata",
        { "state": "PA" },
        "id, state, bill_url"
    )
    for i, bill_row in enumerate(bill_rows):
        url = bill_row.get("bill_url")
        print(f"{i + 1}/{len(bill_rows)} | {url}")
        if not url:
            continue
        html = get_html(url)
        actions = parse_actions(html)
        for action in actions:
            actions_rows.append({
                "bill_id": bill_row.get("id"),
                "state": bill_row.get("state"),
                "action": get_action(
                    action["key"],
                    action["chamber"],
                    action["description"]
                ),
                "date": action["date"],
                "committee": action["committee"],
                "chamber": action["chamber"]
            })
        if (i + 1) % INSERT_BATCH_SIZE == 0:
            insert(
                "bill_actions",
                actions_rows,
                OnDuplicate.MERGE,
                ["bill_id", "date", "action", "chamber", "committee"]
            )
            actions_rows = []
            print('\n')
    insert(
        "bill_actions",
        actions_rows,
        OnDuplicate.MERGE,
        ["bill_id", "date", "action", "chamber", "committee"]
    )
