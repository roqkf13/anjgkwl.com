"""steam_app_id → 외부 모드 소스 식별자 매핑."""

from __future__ import annotations

# Nexus game_domain_name (https://www.nexusmods.com/{domain}/mods/...)
NEXUS_GAME_DOMAIN: dict[int, str] = {
    1245620: "eldenring",
    374320: "darksouls3",
    814380: "sekiro",
    646570: "slaythespire",
    2868840: "slaythespire2",
    292030: "witcher3",
    367520: "hollowknight",
    1145360: "hades",
    2379780: "balatro",
    2215430: "ghostoftsushima",
    261570: "oriandtheblindforest",
    774361: "blasphemous",
    1174180: "reddeadredemption2",
}


def nexus_domain_for(steam_app_id: int) -> str | None:
    return NEXUS_GAME_DOMAIN.get(steam_app_id)
