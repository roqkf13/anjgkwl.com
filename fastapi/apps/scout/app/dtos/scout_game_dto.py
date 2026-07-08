from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ScoutGameDto:
    id: int
    steam_app_id: int
    title: str
    summary: str | None
    genre_id: int | None
    official_site_url: str | None
