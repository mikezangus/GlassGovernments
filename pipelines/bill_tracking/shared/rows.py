from dataclasses import dataclass
from typing import Optional


@dataclass
class BillMetadataRow:
    id: str
    state: str
    session: str
    type: str
    num: str
    bill_url: str
    special_session: Optional[str] = None


@dataclass
class BillActionsRow:
    bill_id: str
    state: str
    action: str
    date: str
    text_url: str


@dataclass
class BillTextsSourceRow:
    id: str
    state: str
    text: str
    

@dataclass
class BillTextsCleanRow:
    id: str
    state: str
    text: str
    

@dataclass
class BillWordsRow:
    id: str
    words: list[str]
    state: str
