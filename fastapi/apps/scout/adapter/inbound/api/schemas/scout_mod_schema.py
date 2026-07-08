from __future__ import annotations

from pydantic import BaseModel, Field


class ScoutModSchema(BaseModel):
    id: int
    game_id: int = Field(..., serialization_alias="gameId")
    mod_kind: str = Field(..., serialization_alias="modKind")
    name: str
    author: str
    summary: str | None = None
    characters: list[str] = []
    source: str | None = None
    source_url: str | None = Field(None, serialization_alias="sourceUrl")
    external_mod_id: str | None = Field(None, serialization_alias="externalModId")

    model_config = {"populate_by_name": True}
