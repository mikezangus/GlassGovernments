from typing import TypedDict


class BillMetadataRow(TypedDict):
    id: str
    state: str
    session: str
    special_session: str | None
    type: str
    bill_num: int
    print_num: int
    bill_url: str
    text_url: str | None
