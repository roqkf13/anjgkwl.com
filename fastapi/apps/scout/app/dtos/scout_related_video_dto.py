from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutRelatedVideoDto:
    id: int
    game_id: int
    title: str
    channel: str
    watch_url: str
    published_at: str | None = None
