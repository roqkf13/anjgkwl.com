from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoutGenreDto:
    id: int
    slug: str
    label: str
    description: str
    traits: list[str] = field(default_factory=list)
    representative_game_id: int | None = None
