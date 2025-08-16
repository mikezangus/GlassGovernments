from alchemy.base import Base
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column


class BillMetadataRow(Base):
    __tablename__ = "bill_metadata"
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )
    state: Mapped[str] = mapped_column(
        String(2),
        nullable=False
    )
    session: Mapped[str] = mapped_column(
        String(2),
        nullable=False
    )
    special_session: Mapped[str] = mapped_column(
        String(16),
        nullable=True
    )
    type: Mapped[str] = mapped_column(
        String(8),
        nullable=False
    )
    num: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    url: Mapped[str] = mapped_column(
        String(512),
        nullable=False
    )
