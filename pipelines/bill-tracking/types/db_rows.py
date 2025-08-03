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


class BillActionsRow(TypedDict):
    id: str
    enacted: bool
    passed_lower: bool
    passed_upper: bool


class BillTextsClean(TypedDict):
    id: str
    text: str
    state: str


class BillTextsSourceRow(TypedDict):
    id: str
    text: str
    state: str


class BillTokensRow(TypedDict):
    id: str
    tokens: list[str]
    state: str
