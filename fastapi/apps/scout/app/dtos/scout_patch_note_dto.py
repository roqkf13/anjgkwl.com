from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ScoutPatchNoteDto:
    id: int
    game_id: int
    external_note_id: str
    source_title: str
    source_summary: str | None
    source_body: str | None
    image_urls: list[str] = field(default_factory=list)
    published_at: str | None = None
    source_url: str | None = None
