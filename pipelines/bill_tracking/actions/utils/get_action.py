from shared.enums import BillAction


def get_action(key: str, chamber: str, description: str) -> str | None:
    match key:
        case _ if key.startswith("introduced"):
            if key.endswith("lower") or chamber.lower() == "lower":
                return BillAction.INTRODUCED_LOWER.value
            if key.endswith("upper") or chamber.lower() == "upper":
                return BillAction.INTRODUCED_UPPER.value
        case "referred_to_committee":
            if chamber == "lower":
                return BillAction.REFERRED_TO_COMMITTEE_LOWER.value
            if chamber == "upper":
                return BillAction.REFERRED_TO_COMMITTEE_UPPER.value
        case "reported_from_committee":
            if chamber == "lower":
                return BillAction.REPORTED_FROM_COMMITTEE_LOWER.value
            if chamber == "upper":
                return BillAction.REPORTED_FROM_COMMITTEE_UPPER.value
        case "third_consideration_passed":
            if chamber == "lower":
                return BillAction.ACCEPTED_LOWER.value
            if chamber == "upper":
                return BillAction.ACCEPTED_UPPER.value
        case "sent_to_governor":
            return BillAction.AT_EXECUTIVE.value
        case "executive_action":
            if description.lower().startswith("approved"):
                return BillAction.ENACTED.value
            return BillAction.VETOED.value
        case "effective":
            return BillAction.ENACTED.value
        
    match description.lower():
        case _ if "referred to committee" in description.lower():
            if chamber == "lower":
                return BillAction.REFERRED_TO_COMMITTEE_LOWER.value
            if chamber == "upper":
                return BillAction.REFERRED_TO_COMMITTEE_UPPER.value
        case "adopted":
            if chamber == "lower":
                return BillAction.ACCEPTED_LOWER.value
            if chamber == "upper":
                return BillAction.ACCEPTED_UPPER.value
        case "offered":
            if chamber == "lower":
                return BillAction.INTRODUCED_LOWER.value
            if chamber == "upper":
                return BillAction.INTRODUCED_UPPER.value
    print(f"No match found for key={key} chamber={chamber} description={description}")
    return None
