def construct_bill_id(state: str, session: int, type: str, bill_num: str) -> str:
    return f"{state}_{session}_{type}_{bill_num}"
