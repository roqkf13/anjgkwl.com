from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

ModKind = Literal["appearance", "functional"]
ModSource = Literal["nexus", "workshop", "curated", "github"]


class PatchContentBlockSchema(BaseModel):
    type: Literal["text", "image"]
    text: str | None = None
    url: str | None = None


class PatchNoteSchema(BaseModel):
    id: str
    title: str
    published_at: str = Field(..., serialization_alias="publishedAt")
    summary: str
    body_ko: str = Field(..., serialization_alias="bodyKo")
    image_urls: list[str] = Field(default_factory=list, serialization_alias="imageUrls")
    content_blocks: list[PatchContentBlockSchema] = Field(
        default_factory=list, serialization_alias="contentBlocks"
    )
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "id": "2358720-steam-5678",
                "title": "Patch 1.5.0",
                "publishedAt": "2025-03-01",
                "summary": "밸런스 조정 및 버그 수정",
                "bodyKo": "이번 패치에서는...",
                "imageUrls": [],
                "contentBlocks": [],
                "sourceUrl": "https://store.steampowered.com/news/...",
            }
        },
    }


class ModSchema(BaseModel):
    id: str
    mod_kind: ModKind = Field(..., serialization_alias="modKind")
    name: str
    author: str
    summary: str
    characters: list[str] = Field(default_factory=list)
    source: ModSource | None = None
    source_url: str | None = Field(default=None, serialization_alias="sourceUrl")

    model_config = {"populate_by_name": True}


class RelatedVideoSchema(BaseModel):
    id: str
    title: str
    channel: str
    published_at: str = Field(..., serialization_alias="publishedAt")
    watch_url: str = Field(..., serialization_alias="watchUrl")

    model_config = {"populate_by_name": True}


class GameDetailSchema(BaseModel):
    steam_app_id: int = Field(..., serialization_alias="steamAppId")
    title: str
    steam_store_url: str = Field(..., serialization_alias="steamStoreUrl")
    official_site_url: str = Field(..., serialization_alias="officialSiteUrl")
    patch_notes: list[PatchNoteSchema] = Field(
        default_factory=list, serialization_alias="patchNotes"
    )
    appearance_mods: list[ModSchema] = Field(
        default_factory=list, serialization_alias="appearanceMods"
    )
    functional_mods: list[ModSchema] = Field(
        default_factory=list, serialization_alias="functionalMods"
    )
    videos: list[RelatedVideoSchema] = Field(default_factory=list)

    model_config = {
        "populate_by_name": True,
        "json_schema_extra": {
            "example": {
                "steamAppId": 2358720,
                "title": "Slay the Spire 2",
                "steamStoreUrl": "https://store.steampowered.com/app/2358720",
                "officialSiteUrl": "https://www.megacrit.com",
                "patchNotes": [],
                "appearanceMods": [],
                "functionalMods": [],
                "videos": [],
            }
        },
    }
