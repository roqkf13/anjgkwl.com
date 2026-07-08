from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PortType(Enum):
    CHERBOURG = "C"
    QUEENSTOWN = "Q"
    SOUTHAMPTON = "S"


@dataclass(frozen=True, slots=True)
class Embarked:
    value: PortType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Embarked":
        if not raw or not raw.strip():
            raise ValueError("탑승 항구는 필수 값입니다.")
        normalized = raw.strip().upper()
        try:
            return cls(PortType(normalized))
        except ValueError:
            raise ValueError(f"유효하지 않은 탑승 항구입니다: {raw!r}")

    def __str__(self) -> str:
        return self.value.value
