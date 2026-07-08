from __future__ import annotations

from pydantic import BaseModel, Field


class ScoutGenreSchema(BaseModel):
    id: int
    slug: str
    label: str
    description: str
    traits: list[str] = []
    representative_game_id: int | None = Field(None, serialization_alias="representativeGameId")

    model_config = {"populate_by_name": True}


class GenreGameSchema(BaseModel):
    title: str = Field(..., min_length=1)
    summary: str = Field(default="")
    steam_app_id: int = Field(..., ge=1, serialization_alias="steamAppId")

    model_config = {"populate_by_name": True}


class GenreHubSchema(BaseModel):
    id: str
    label: str
    description: str
    representative_title: str = Field(..., serialization_alias="representativeTitle")
    traits: list[str]
    games: list[GenreGameSchema]

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "soulslike",
                "label": "소울라이크",
                "description": "높은 난이도와 정밀한 전투 메카닉",
                "representativeTitle": "Elden Ring",
                "traits": ["high difficulty", "precise combat"],
                "games": [{"title": "Elden Ring", "summary": "...", "steamAppId": 1245620}],
            }
        },
    }
