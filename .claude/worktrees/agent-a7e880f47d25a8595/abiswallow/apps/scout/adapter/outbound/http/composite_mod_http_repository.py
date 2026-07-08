"""큐레이션 + Nexus + Workshop 결과를 appearance/functional 로 나눈다."""

from __future__ import annotations

import asyncio
import logging

from scout.adapter.outbound.http.nexus_mod_http_repository import (
    NexusModHttpRepository,
)
from scout.adapter.outbound.http.workshop_mod_http_repository import (
    WorkshopModHttpRepository,
)
from scout.adapter.outbound.http.mod_game_mapping import nexus_domain_for
from scout.adapter.outbound.static.curated_appearance_mod_repository import (
    CuratedAppearanceModRepository,
)
from scout.app.dtos.game_detail_dto import ModDto
from scout.app.ports.output.mod_repository import ModRepository
from scout.domain.mod_character_rules import infer_mod_characters
from scout.domain.mod_source_url import resolve_mod_source_url

logger = logging.getLogger(__name__)


def _split_by_kind(
    mods: list[ModDto], *, limit_per_kind: int
) -> tuple[list[ModDto], list[ModDto]]:
    appearance: list[ModDto] = []
    functional: list[ModDto] = []
    for mod in mods:
        if mod.mod_kind == "appearance" and len(appearance) < limit_per_kind:
            appearance.append(mod)
        elif mod.mod_kind == "functional" and len(functional) < limit_per_kind:
            functional.append(mod)
        if len(appearance) >= limit_per_kind and len(functional) >= limit_per_kind:
            break
    return appearance, functional


def _ensure_mod_characters(mod: ModDto) -> ModDto:
    if mod.characters:
        return mod
    return mod.model_copy(
        update={"characters": infer_mod_characters(mod.name, mod.summary)}
    )


def _dedupe_mods(mods: list[ModDto]) -> list[ModDto]:
    seen: set[str] = set()
    out: list[ModDto] = []
    for mod in mods:
        key = mod.id.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(mod)
    return out


def _merge_appearance_mods(
    curated: list[ModDto],
    remote: list[ModDto],
    *,
    limit: int,
) -> list[ModDto]:
    """큐레이션을 우선, API 결과로 빈 자리·중복 없는 항목만 보강."""
    merged = _dedupe_mods([*curated, *remote])
    appearance = [m for m in merged if m.mod_kind == "appearance"]
    return appearance[:limit]


class CompositeModHttpRepository(ModRepository):
    def __init__(
        self,
        *,
        nexus: NexusModHttpRepository | None = None,
        workshop: WorkshopModHttpRepository | None = None,
        curated: CuratedAppearanceModRepository | None = None,
    ) -> None:
        self._nexus = nexus or NexusModHttpRepository()
        self._workshop = workshop or WorkshopModHttpRepository()
        self._curated = curated or CuratedAppearanceModRepository()

    async def fetch_mods_for_game(
        self, steam_app_id: int, *, limit_per_kind: int = 8
    ) -> tuple[list[ModDto], list[ModDto]]:
        per_source = max(limit_per_kind, 8)
        nexus_task = self._nexus.fetch_mods(steam_app_id, limit=per_source)
        workshop_task = self._workshop.fetch_mods(steam_app_id, limit=per_source)
        curated_appearance = self._curated.fetch_appearance_mods(steam_app_id)
        nexus_mods, workshop_mods = await asyncio.gather(nexus_task, workshop_task)
        merged_remote = _dedupe_mods([*nexus_mods, *workshop_mods])
        remote_appearance, functional = _split_by_kind(
            merged_remote, limit_per_kind=limit_per_kind
        )
        appearance = _merge_appearance_mods(
            curated_appearance,
            remote_appearance,
            limit=max(limit_per_kind, len(curated_appearance)),
        )
        domain = nexus_domain_for(steam_app_id)
        appearance = [
            _ensure_mod_characters(
                resolve_mod_source_url(mod, nexus_game_domain=domain)
            )
            for mod in appearance
        ]
        functional = [
            _ensure_mod_characters(
                resolve_mod_source_url(mod, nexus_game_domain=domain)
            )
            for mod in functional
        ]

        logger.info(
            "[CompositeModHttpRepository] steam_app_id=%s "
            "curated=%s nexus=%s workshop=%s appearance=%s functional=%s",
            steam_app_id,
            len(curated_appearance),
            len(nexus_mods),
            len(workshop_mods),
            len(appearance),
            len(functional),
        )
        return appearance, functional
