"""SCOUT_MODS — 게임별 모드 메타 (ERD)."""

from typing import Literal

from pydantic import BaseModel, Field

ModKind = Literal["appearance", "functional"]
ModSource = Literal["nexus", "workshop", "curated", "github"]


class ScoutModSchema(BaseModel):
    id: int | None = None
    game_id: int = Field(..., serialization_alias="gameId")
    mod_kind: ModKind = Field(..., serialization_alias="modKind")
    name: str
    author: str
    summary: str = ""
    characters: list[str] = Field(default_factory=list)
    source: ModSource | None = None
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")
    external_mod_id: str | None = Field(
        default=None, serialization_alias="externalModId"
    )

    model_config = {"populate_by_name": True}
