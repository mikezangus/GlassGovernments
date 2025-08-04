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
    in_lower: bool | None
    passed_lower: bool | None
    rejected_lower: bool | None
    committee_lower: str | None
    in_upper: bool | None
    passed_upper: bool | None
    rejected_upper: bool | None
    committee_upper: str | None
    at_executive: bool | None
    enacted: bool | None
    timestamp: str | None


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
