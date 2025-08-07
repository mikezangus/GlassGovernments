from dataclasses import dataclass


@dataclass
class BillMetadataRow:
    id: str
    state: str
    session: str
    special_session: str | None
    type: str
    bill_num: int
    print_num: int | None
    bill_url: str
    text_url: str | None
