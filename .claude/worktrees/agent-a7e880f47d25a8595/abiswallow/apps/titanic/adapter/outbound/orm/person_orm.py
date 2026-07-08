from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from titanic.adapter.outbound.orm.base import Base


class Person(Base):
    """3NF Person — james_director_dto.PersonCommand."""

    __tablename__ = "titanic_person"

    passenger_id: Mapped[str] = mapped_column(String(32), primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, default="")
    gender: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    age: Mapped[str] = mapped_column(String(16), nullable=False, default="")
    sib_sp: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    parch: Mapped[str] = mapped_column(String(8), nullable=False, default="")
    survived: Mapped[str] = mapped_column(String(8), nullable=False, default="")
