from ....db.alchemy.models.bill_actions import BillActionType


def get_action(key: str, chamber: str, description: str) -> str | None:
    match key:
        case _ if key.startswith("introduced"):
            if key.endswith("lower") or chamber.lower() == "lower":
                return BillActionType.INTRODUCED_LOWER.value
            if key.endswith("upper") or chamber.lower() == "upper":
                return BillActionType.INTRODUCED_UPPER.value
        case "referred_to_committee":
            if chamber == "lower":
                return BillActionType.REFERRED_LOWER.value
            if chamber == "upper":
                return BillActionType.REFERRED_UPPER.value
        case "reported_from_committee":
            if chamber == "lower":
                return BillActionType.REPORTED_LOWER.value
            if chamber == "upper":
                return BillActionType.REPORTED_UPPER.value
        case "third_consideration_passed":
            if chamber == "lower":
                return BillActionType.PASSED_LOWER.value
            if chamber == "upper":
                return BillActionType.PASSED_UPPER.value
        case "sent_to_governor":
            return BillActionType.INTRODUCED_EXECUTIVE.value
        case "executive_action":
            if description.lower().startswith("approved"):
                return BillActionType.PASSED_EXECUTIVE.value
            return BillActionType.REJECTED_EXECUTIVE.value
        case "effective":
            return BillActionType.ENACTED.value
        
    match description.lower():
        case _ if "referred to committee" in description.lower():
            if chamber == "lower":
                return BillActionType.REFERRED_LOWER.value
            if chamber == "upper":
                return BillActionType.REFERRED_UPPER.value
        case "adopted":
            if chamber == "lower":
                return BillActionType.PASSED_LOWER.value
            if chamber == "upper":
                return BillActionType.PASSED_UPPER.value
        case "offered":
            if chamber == "lower":
                return BillActionType.INTRODUCED_LOWER.value
            if chamber == "upper":
                return BillActionType.INTRODUCED_UPPER.value
    print(f"No match found for key={key} chamber={chamber} description={description}")
    return None
