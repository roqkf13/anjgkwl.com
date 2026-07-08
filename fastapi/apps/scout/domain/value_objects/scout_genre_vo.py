from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class GenreSlug:
    value: str

    def __post_init__(self) -> None:
        cleaned = (self.value or "").strip().lower()
        if not cleaned:
            raise ValueError("GenreSlug는 비어 있을 수 없습니다.")
        object.__setattr__(self, "value", cleaned)


@dataclass(frozen=True, slots=True)
class GenreLabel:
    value: str

    def __post_init__(self) -> None:
        if not (self.value or "").strip():
            raise ValueError("GenreLabel은 비어 있을 수 없습니다.")
