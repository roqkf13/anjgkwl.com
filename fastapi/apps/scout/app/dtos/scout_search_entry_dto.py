from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class VideoLinkDto:
    title: str
    channel: str
    watch_url: str
    published_at: str | None = None


@dataclass(frozen=True)
class ScoutSearchEntryDto:
    id: int
    query_key: str
    title: str
    platform: str | None
    summary: str | None
    official_site_url: str | None
    videos: list[VideoLinkDto]
