from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from titanic.adapter.outbound.orm.base import Base


class Booking(Base):
    """Booking — james_director_dto.BookingCommand (+ FK to Person)."""

    __tablename__ = "titanic_booking"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey("titanic_person.passenger_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    pclass: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    ticket: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    fare: Mapped[str] = mapped_column(String(32), nullable=False, default="")
    cabin: Mapped[str] = mapped_column(String(64), nullable=False, default="")
    embarked: Mapped[str] = mapped_column(String(8), nullable=False, default="")
