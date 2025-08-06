from dataclasses import dataclass
from enum import Enum


class LegislationType(str, Enum):
    HOUSE_BILL = "House Bill"
    SENATE_BILL = "Senate Bill"
    HOUSE_RESOLUTION = "House Resolution"
    SENATE_RESOLUTION = "Senate Resolution"
    HOUSE_CONCURRENT_RESOLUTION = "House Concurrent Resolution"
    SENATE_CONCURRENT_RESOLUTION = "Senate Concurrent Resolution"
    HOUSE_JOINT_RESOLUTION = "House Joint Resolution"
    SENATE_JOINT_RESOLUTION = "Senate Joint Resolution"


@dataclass
class BillMetadata:
    state: str
    session: str
    type: str
    bill_num: str
    bill_url: str
