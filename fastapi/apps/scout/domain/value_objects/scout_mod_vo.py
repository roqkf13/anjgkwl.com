from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ModKind(Enum):
    APPEARANCE = "appearance"
    FUNCTIONAL = "functional"


class ModSource(Enum):
    NEXUS = "nexus"
    WORKSHOP = "workshop"
    CURATED = "curated"
    GITHUB = "github"


@dataclass(frozen=True, slots=True)
class CharacterSlug:
    value: str  # regent / silent / ironclad / defect / necrobinder / other

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip().lower()
        if not cleaned:
            raise ValueError("CharacterSlug는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class ExternalModId:
    value: str

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("ExternalModId는 비어 있을 수 없습니다.")
