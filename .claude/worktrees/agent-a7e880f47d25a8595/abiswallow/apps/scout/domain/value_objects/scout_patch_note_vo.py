from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BlockType(Enum):
    TEXT = "text"
    IMAGE = "image"


@dataclass(frozen=True, slots=True)
class ExternalNoteId:
    value: str  # e.g. "1245620-steam-12345678"

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("ExternalNoteId는 비어 있을 수 없습니다.")


@dataclass(frozen=True, slots=True)
class Locale:
    value: str  # e.g. "ko-KR"

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("Locale은 비어 있을 수 없습니다.")
