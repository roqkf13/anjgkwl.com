from __future__ import annotations

from pydantic import BaseModel, Field


class ScoutSearchVideoSchema(BaseModel):
    title: str
    channel: str
    watch_url: str = Field(..., serialization_alias="watchUrl")
    published_at: str | None = Field(None, serialization_alias="publishedAt")

    model_config = {"populate_by_name": True}


class ScoutSearchEntrySchema(BaseModel):
    id: int
    query_key: str = Field(..., serialization_alias="queryKey")
    title: str
    platform: str | None = None
    summary: str | None = None
    official_site_url: str | None = Field(None, serialization_alias="officialSiteUrl")
    videos: list[ScoutSearchVideoSchema] = []

    model_config = {"populate_by_name": True}
