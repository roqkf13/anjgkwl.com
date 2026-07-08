from __future__ import annotations

from pydantic import BaseModel, Field


class ScoutRelatedVideoSchema(BaseModel):
    id: int
    game_id: int = Field(..., serialization_alias="gameId")
    title: str
    channel: str
    watch_url: str = Field(..., serialization_alias="watchUrl")
    published_at: str | None = Field(None, serialization_alias="publishedAt")

    model_config = {"populate_by_name": True}
