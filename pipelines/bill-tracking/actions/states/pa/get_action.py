from shared.enums import BillAction


def get_action(key: str, chamber: str, description: str) -> str:
    match key:
        case _ if key.startswith("introduced"):
            if key.endswith("lower"):
                return BillAction.INTRODUCED_LOWER.value
            if key.endswith("upper"):
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
        case "executive_action":
            if description.lower().startswith("approved"):
                return BillAction.ENACTED.value
            return BillAction.VETOED.value
    raise ValueError(f"Failed to get action: key={key} chamber={chamber} description={description}")
