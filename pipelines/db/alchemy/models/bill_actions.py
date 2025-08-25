import uuid
from enum import auto, Enum
from sqlalchemy import String, Date, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from ..base import Base


class Chamber(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()
    
    lower = auto()
    upper = auto()
    executive = auto()


class BillActionType(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name.lower()
    
    INTRODUCED_LOWER = auto()
    REFERRED_LOWER = auto()
    REPORTED_LOWER = auto()
    PASSED_LOWER = auto()
    REJECTED_LOWER = auto()
    TABLED_LOWER = auto()
    REMOVED_FROM_TABLE_LOWER = auto()

    INTRODUCED_UPPER = auto()
    REFERRED_UPPER = auto()
    REPORTED_UPPER = auto()
    PASSED_UPPER = auto()
    REJECTED_UPPER = auto()
    TABLED_UPPER = auto()
    REMOVED_FROM_TABLE_UPPER = auto()

    INTRODUCED_EXECUTIVE = auto()
    PASSED_EXECUTIVE = auto()
    REJECTED_EXECUTIVE = auto()

    ENACTED = auto()
    WITHDRAWN = auto()


class BillActionsRow(Base):
    __tablename__ = "bill_actions"
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    action: Mapped[BillActionType] = mapped_column(
        SAEnum(BillActionType, name="bill_action_type"),
        nullable=False
    )
    date: Mapped[Date] = mapped_column(
        Date,
        nullable=False
    )
    committee: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True
    )
    chamber: Mapped[Chamber] = mapped_column(
        SAEnum(Chamber, name="chamber"),
        nullable=False
    )
    __table_args__ = ()
