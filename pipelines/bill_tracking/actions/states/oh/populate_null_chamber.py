from shared.rows import BillAction


def populate_null_chamber(key: str) -> str | None:
    print("attempting to populate:", key)
    executive_actions = (
        BillAction.AT_EXECUTIVE.value,
        BillAction.LINE_ITEM_VETO.value,
        BillAction.SIGNED_BY_GOVERNOR.value,
        BillAction.VETOED.value
    )
    if key in executive_actions:
        return "executive"
