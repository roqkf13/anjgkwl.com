from __future__ import annotations

from pydantic import BaseModel, Field


class ScoutGameSchema(BaseModel):
    id: int
    steam_app_id: int = Field(..., serialization_alias="steamAppId")
    title: str
    summary: str | None = None
    genre_id: int | None = Field(None, serialization_alias="genreId")
    official_site_url: str | None = Field(None, serialization_alias="officialSiteUrl")

    model_config = {"populate_by_name": True}
