"""정적 큐레이션 외형 모드 조회."""

from __future__ import annotations

from scout.adapter.outbound.http.mod_game_mapping import nexus_domain_for
from scout.adapter.outbound.static.curated_appearance_mods import (
    curated_appearance_mods_for,
)
from scout.app.dtos.game_detail_dto import ModDto
from scout.domain.mod_source_url import resolve_mod_source_url


class CuratedAppearanceModRepository:
    def fetch_appearance_mods(self, steam_app_id: int) -> list[ModDto]:
        domain = nexus_domain_for(steam_app_id)
        return [
            resolve_mod_source_url(mod, nexus_game_domain=domain)
            for mod in curated_appearance_mods_for(steam_app_id)
        ]
