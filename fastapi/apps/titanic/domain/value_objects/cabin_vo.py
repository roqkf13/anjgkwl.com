from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True, slots=True)
class Cabin:
    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip()
        if not cleaned:
            raise ValueError("객실 번호는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class CabinAssigned:
    """객실 배정 여부. 결측치 자체가 3등석 미배정 승객을 나타내는 신호다."""

    value: bool

    @classmethod
    def from_cabin(cls, cabin: Optional[str]) -> "CabinAssigned":
        return cls(bool(cabin and cabin.strip()))

    @property
    def as_feature(self) -> int:
        """ML 피처값: 배정됨=1, 미배정=0."""
        return 1 if self.value else 0
