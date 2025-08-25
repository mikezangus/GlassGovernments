from .....db.alchemy.models.bill_actions import BillActionType


def populate_null_chamber(key: str) -> str | None:
    executive_actions = (
        BillActionType.INTRODUCED_EXECUTIVE.value,
        BillActionType.PASSED_EXECUTIVE.value,
        BillActionType.REJECTED_EXECUTIVE.value
    )
    if key in executive_actions:
        return "executive"
