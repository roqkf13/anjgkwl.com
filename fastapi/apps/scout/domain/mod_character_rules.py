"""모드가 대상으로 하는 플레이어블 캐릭터 슬러그·추론."""

from __future__ import annotations

ModCharacterSlug = str

# STS2 roster (Sts2SkinManager 기준)
STS2_CHARACTERS: tuple[ModCharacterSlug, ...] = (
    "regent",
    "silent",
    "ironclad",
    "defect",
    "necrobinder",
)

_CHARACTER_KEYWORDS: dict[ModCharacterSlug, tuple[str, ...]] = {
    "regent": ("regent", "리젠트", "储君", "princess regent"),
    "silent": ("silent", "사일런트"),
    "ironclad": ("ironclad", "아이언클래드", "철권"),
    "defect": ("defect", "디펙트", "缺省"),
    "necrobinder": ("necrobinder", "네크로바인더", "necro", "骨妹"),
}

_GAME_CHARACTERS: dict[int, tuple[ModCharacterSlug, ...]] = {
    2868840: STS2_CHARACTERS,
}


def characters_for_game(steam_app_id: int) -> tuple[ModCharacterSlug, ...]:
    return _GAME_CHARACTERS.get(steam_app_id, ())


def infer_mod_characters(
    name: str,
    summary: str,
    *,
    tags: list[str] | None = None,
) -> list[ModCharacterSlug]:
    text = " ".join([name, summary, *(tags or [])]).lower()
    found: list[ModCharacterSlug] = []
    for slug, keywords in _CHARACTER_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            found.append(slug)
    if found:
        return found
    return ["other"]
