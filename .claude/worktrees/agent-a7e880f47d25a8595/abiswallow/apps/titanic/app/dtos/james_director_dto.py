from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True, slots=True, kw_only=True)
class PersonCommand:
    """3NF Person — 식별자·FK 뒤 승객 속성."""

    passenger_id: str
    name: str
    gender: str
    age: str
    sib_sp: str
    parch: str
    survived: str


@dataclass(frozen=True, slots=True, kw_only=True)
class BookingCommand:
    """Booking에 Port(embarked_code, port_name)를 합친 역정규화. country는 제외."""

    pclass: str
    ticket: str
    fare: str
    cabin: str
    embarked: str


def _field(row: Mapping[str, Any], key: str) -> str:
    return str(row.get(key) or "")


def commands_from_upload_record(
    record: Mapping[str, Any],
) -> tuple[PersonCommand, BookingCommand] | None:
    """업로드 행 dict → Person/Booking 커맨드. passenger_id 없으면 None."""
    passenger_id = _field(record, "passenger_id")
    if not passenger_id:
        return None
    return (
        PersonCommand(
            passenger_id=passenger_id,
            name=_field(record, "name"),
            gender=_field(record, "gender"),
            age=_field(record, "age"),
            sib_sp=_field(record, "sib_sp"),
            parch=_field(record, "parch"),
            survived=_field(record, "survived"),
        ),
        BookingCommand(
            pclass=_field(record, "pclass"),
            ticket=_field(record, "ticket"),
            fare=_field(record, "fare"),
            cabin=_field(record, "cabin"),
            embarked=_field(record, "embarked"),
        ),
    )

