from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoutModDto:
    id: int
    game_id: int
    mod_kind: str
    name: str
    author: str
    summary: str | None
    characters: list[str] = field(default_factory=list)
    source: str | None = None
    source_url: str | None = None
    external_mod_id: str | None = None
