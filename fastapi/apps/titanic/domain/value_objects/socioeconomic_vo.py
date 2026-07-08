from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# PClass
# ---------------------------------------------------------------------------

class PClassType(int, Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3


@dataclass(frozen=True, slots=True)
class PClass:
    value: PClassType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "PClass":
        if raw is None or raw.strip() == "":
            raise ValueError("PClass는 필수 값입니다.")
        try:
            return cls(value=PClassType(int(raw.strip())))
        except (ValueError, KeyError):
            raise ValueError(f"PClass 유효하지 않은 값: '{raw}'")

    @classmethod
    def from_int(cls, value: int) -> "PClass":
        try:
            return cls(value=PClassType(value))
        except ValueError:
            raise ValueError(f"PClass 유효하지 않은 값: {value}")

    @property
    def is_first_class(self) -> bool:
        return self.value == PClassType.FIRST

    @property
    def is_third_class(self) -> bool:
        return self.value == PClassType.THIRD

    @property
    def label(self) -> str:
        return {
            PClassType.FIRST: "1등석",
            PClassType.SECOND: "2등석",
            PClassType.THIRD: "3등석",
        }[self.value]

    @property
    def has_lifeboat_priority(self) -> bool:
        """1등석 승객은 구명보트 탑승 우선순위가 높았다."""
        return self.value == PClassType.FIRST

    def __str__(self) -> str:
        return str(self.value.value)


# ---------------------------------------------------------------------------
# Fare
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class Fare:
    value: float

    def __post_init__(self) -> None:
        if self.value < 0:
            raise ValueError(f"요금은 음수일 수 없습니다: {self.value}")

    @classmethod
    def from_raw(cls, raw: str) -> "Fare":
        return cls(float(raw.strip()))


class FareBinType(Enum):
    VERY_LOW = "very_low"   # 0 ~ 7.91
    LOW = "low"             # 7.91 ~ 14.45
    MEDIUM = "medium"       # 14.45 ~ 31.0
    HIGH = "high"           # > 31.0


@dataclass(frozen=True, slots=True)
class FareBin:
    """운임 구간화 파생 피처 (비대칭 분포 처리)."""

    value: FareBinType

    @classmethod
    def from_fare(cls, fare: float) -> "FareBin":
        # 경계값은 Kaggle Titanic 운임 사분위수 기준 (문서 미명시, 추후 조정 가능)
        if fare < 0:
            raise ValueError(f"운임은 음수일 수 없습니다: {fare}")
        if fare < 7.91:
            return cls(FareBinType.VERY_LOW)
        if fare < 14.45:
            return cls(FareBinType.LOW)
        if fare < 31.0:
            return cls(FareBinType.MEDIUM)
        return cls(FareBinType.HIGH)


# ---------------------------------------------------------------------------
# SocioeconomicStatus  —  Embedded Type
# 객실 등급과 운임은 모두 경제적 지위를 나타내는 지표로 함께 관리한다.
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class SocioeconomicStatus:
    """객실 등급과 운임을 함께 보유하는 임베디드 값 타입."""

    pclass: PClass
    fare: Fare

    @classmethod
    def from_raw(cls, pclass_raw: int, fare_raw: float) -> "SocioeconomicStatus":
        return cls(
            pclass=PClass.from_int(pclass_raw),
            fare=Fare(fare_raw),
        )

    @property
    def pclass_encoded(self) -> int:
        return int(self.pclass.value)

    @property
    def fare_value(self) -> float:
        return self.fare.value

    @property
    def fare_bin(self) -> FareBin:
        return FareBin.from_fare(self.fare.value)
