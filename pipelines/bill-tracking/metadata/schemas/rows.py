from dataclasses import dataclass
from typing import Optional


@dataclass
class BillMetadataRow:
    id: str
    state: str
    session: int
    type: str
    bill_num: int
    bill_url: str
    special_session: Optional[str] = None
    print_num: Optional[int] = None
    text_url: Optional[str] = None
