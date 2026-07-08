from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Gender
# ---------------------------------------------------------------------------

class GenderType(Enum):
    MALE = "male"
    FEMALE = "female"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class Gender:
    value: GenderType

    @classmethod
    def from_raw(cls, raw: Optional[str]) -> "Gender":
        if raw is None:
            return cls(GenderType.UNKNOWN)
        normalized = raw.strip().lower()
        if normalized == "male":
            return cls(GenderType.MALE)
        if normalized == "female":
            return cls(GenderType.FEMALE)
        return cls(GenderType.UNKNOWN)

    @property
    def is_female(self) -> bool:
        return self.value == GenderType.FEMALE

    @property
    def is_unknown(self) -> bool:
        return self.value == GenderType.UNKNOWN


# ---------------------------------------------------------------------------
# Title
# ---------------------------------------------------------------------------

_RARE_TITLES: frozenset[str] = frozenset({
    "Capt", "Col", "Don", "Dr", "Major", "Rev", "Jonkheer", "Dona", "Mme",
})
_ROYAL_TITLES: frozenset[str] = frozenset({"Countess", "Lady", "Sir"})
_NORMALIZE_MAP: dict[str, str] = {"Mlle": "Mr", "Ms": "Miss"}

# crew_lowe_boat_interactor.py title_mapping 기준
_ORDINAL_MAP: dict[str, int] = {
    "Mr": 1, "Miss": 2, "Mrs": 3, "Master": 4, "Royal": 5, "Rare": 6,
}


class TitleType(Enum):
    UNKNOWN = "Unknown"
    MR = "Mr"
    MISS = "Miss"
    MRS = "Mrs"
    MASTER = "Master"
    ROYAL = "Royal"
    RARE = "Rare"


@dataclass(frozen=True, slots=True)
class Title:
    value: TitleType

    @classmethod
    def from_name(cls, name: Optional[str]) -> "Title":
        if not name:
            return cls(TitleType.UNKNOWN)
        match = re.search(r"([A-Za-z]+)\.", name)
        if not match:
            return cls(TitleType.UNKNOWN)
        raw = match.group(1)
        if raw in _RARE_TITLES:
            return cls(TitleType.RARE)
        if raw in _ROYAL_TITLES:
            return cls(TitleType.ROYAL)
        raw = _NORMALIZE_MAP.get(raw, raw)
        try:
            return cls(TitleType(raw))
        except ValueError:
            return cls(TitleType.UNKNOWN)

    @property
    def ordinal(self) -> int:
        """title_mapping 기준 정수 인코딩. 미매핑 호칭은 0."""
        return _ORDINAL_MAP.get(self.value.value, 0)

    @property
    def is_master(self) -> bool:
        """Master는 어린 남성 — Age 결측치 대체 시 기준으로 사용된다."""
        return self.value == TitleType.MASTER

    @property
    def is_rare(self) -> bool:
        return self.value == TitleType.RARE

    @property
    def is_royal(self) -> bool:
        return self.value == TitleType.ROYAL


# ---------------------------------------------------------------------------
# PassengerIdentity  —  Embedded Type
# 호칭(Title)은 성별·사회적 지위를 내포하므로 Gender와 함께 관리한다.
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class PassengerIdentity:
    """성별과 호칭을 함께 보유하는 임베디드 값 타입."""

    gender: Gender
    title: Title

    @classmethod
    def from_raw(cls, name: Optional[str], gender_raw: Optional[str]) -> "PassengerIdentity":
        return cls(
            gender=Gender.from_raw(gender_raw),
            title=Title.from_name(name),
        )

    @property
    def is_female(self) -> bool:
        return self.gender.is_female

    @property
    def gender_encoded(self) -> int:
        """female=1, male=0, unknown=0."""
        return 1 if self.gender.is_female else 0

    @property
    def title_ordinal(self) -> int:
        return self.title.ordinal
