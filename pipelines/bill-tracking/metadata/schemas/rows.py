from dataclasses import dataclass
from typing import Optional


@dataclass
class BillMetadata:
    id: str
    state: str
    session: str
    type: str
    bill_num: str
    bill_url: str
    special_session: Optional[str] = None
    print_num: Optional[str] = None
    text_url: Optional[str] = None
