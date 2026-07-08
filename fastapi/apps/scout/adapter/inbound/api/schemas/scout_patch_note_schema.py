from __future__ import annotations

from pydantic import BaseModel, Field


class ScoutPatchNoteSchema(BaseModel):
    id: int
    game_id: int = Field(..., serialization_alias="gameId")
    external_note_id: str = Field(..., serialization_alias="externalNoteId")
    source_title: str = Field(..., serialization_alias="sourceTitle")
    source_summary: str | None = Field(None, serialization_alias="sourceSummary")
    source_body: str | None = Field(None, serialization_alias="sourceBody")
    image_urls: list[str] = Field(default_factory=list, serialization_alias="imageUrls")
    published_at: str | None = Field(None, serialization_alias="publishedAt")
    source_url: str | None = Field(None, serialization_alias="sourceUrl")

    model_config = {"populate_by_name": True}
