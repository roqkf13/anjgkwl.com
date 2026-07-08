"""모드 메타(제목·설명·태그)로 외형/기능을 휴리스틱 분류한다."""

from __future__ import annotations

from scout.app.dtos.game_detail_dto import ModKind

_APPEARANCE_KEYWORDS = (
    "skin",
    "reskin",
    "texture",
    "portrait",
    "card art",
    "sprite",
    "model",
    "cosmetic",
    "visual",
    "appearance",
    "outfit",
    "voice",
    "art pack",
    "ui",
)

_FUNCTIONAL_KEYWORDS = (
    "character",
    "playable",
    "class",
    "balance",
    "gameplay",
    "quality of life",
    "qol",
    "multiplayer",
    "framework",
    "mod loader",
    "expansion",
    "mechanic",
)


def classify_mod_kind(
    name: str,
    summary: str,
    *,
    tags: list[str] | None = None,
) -> ModKind:
    text = " ".join([name, summary, *(tags or [])]).lower()
    if any(keyword in text for keyword in _APPEARANCE_KEYWORDS):
        return "appearance"
    if any(keyword in text for keyword in _FUNCTIONAL_KEYWORDS):
        return "functional"
    return "functional"
