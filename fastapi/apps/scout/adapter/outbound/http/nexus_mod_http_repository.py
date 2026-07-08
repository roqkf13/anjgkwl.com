"""Nexus Mods API에서 게임별 트렌딩 모드를 가져온다."""

from __future__ import annotations

import asyncio
import logging
import os
import re
from typing import Any

from scout.adapter.outbound.http.http_json_client import build_url, fetch_json
from scout.adapter.outbound.http.mod_game_mapping import nexus_domain_for
from scout.app.dtos.game_detail_dto import ModDto
from scout.domain.mod_character_rules import infer_mod_characters
from scout.domain.mod_kind_rules import classify_mod_kind

logger = logging.getLogger(__name__)

_NEXUS_API_BASE = "https://api.nexusmods.com/v1"
_DEFAULT_LIMIT = 10
_SUMMARY_MAX = 280


def _nexus_api_key() -> str:
    return os.getenv("NEXUS_API_KEY", "").strip()


def _plain_text(raw: str) -> str:
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _author_name(item: dict[str, Any]) -> str:
    user = item.get("user")
    if isinstance(user, dict):
        name = (user.get("name") or "").strip()
        if name:
            return name
    for key in ("author", "username", "uploader"):
        value = (item.get(key) or "").strip()
        if value:
            return value
    return "Nexus Mods"


def _summary_text(item: dict[str, Any]) -> str:
    for key in ("summary", "description", "brief_description"):
        raw = (item.get(key) or "").strip()
        if raw:
            text = _plain_text(raw)
            if len(text) > _SUMMARY_MAX:
                return text[: _SUMMARY_MAX - 1] + "…"
            return text
    return "Nexus Mods에서 제공하는 모드입니다."


def _mod_id(item: dict[str, Any]) -> str | None:
    for key in ("mod_id", "modId", "id"):
        value = item.get(key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def _parse_mod_list(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if not isinstance(payload, dict):
        return []
    for key in ("results", "mods", "data"):
        value = payload.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def _to_mod_dto(
    *,
    steam_app_id: int,
    game_domain: str,
    item: dict[str, Any],
) -> ModDto | None:
    mod_id = _mod_id(item)
    name = (item.get("name") or "").strip()
    if not mod_id or not name:
        return None
    summary = _summary_text(item)
    tags = item.get("tags")
    tag_list = [str(t) for t in tags] if isinstance(tags, list) else None
    return ModDto(
        id=f"{steam_app_id}-nexus-{mod_id}",
        mod_kind=classify_mod_kind(name, summary, tags=tag_list),
        name=name,
        author=_author_name(item),
        summary=summary,
        characters=infer_mod_characters(name, summary, tags=tag_list),
        source="nexus",
        source_url=f"https://www.nexusmods.com/{game_domain}/mods/{mod_id}",
    )


class NexusModHttpRepository:
    async def fetch_mods(
        self, steam_app_id: int, *, limit: int = _DEFAULT_LIMIT
    ) -> list[ModDto]:
        return await asyncio.to_thread(self._fetch_sync, steam_app_id, limit)

    def _fetch_sync(self, steam_app_id: int, limit: int) -> list[ModDto]:
        api_key = _nexus_api_key()
        if not api_key:
            logger.info(
                "[NexusModHttpRepository] skip steam_app_id=%s (NEXUS_API_KEY missing)",
                steam_app_id,
            )
            return []

        game_domain = nexus_domain_for(steam_app_id)
        if not game_domain:
            logger.info(
                "[NexusModHttpRepository] skip steam_app_id=%s (no nexus domain mapping)",
                steam_app_id,
            )
            return []

        url = build_url(
            f"{_NEXUS_API_BASE}/games/{game_domain}/mods/trending.json",
            {},
        )
        payload = fetch_json(url, headers={"apikey": api_key})
        if payload is None:
            return []

        mods: list[ModDto] = []
        for item in _parse_mod_list(payload)[:limit]:
            dto = _to_mod_dto(
                steam_app_id=steam_app_id,
                game_domain=game_domain,
                item=item,
            )
            if dto:
                mods.append(dto)

        logger.info(
            "[NexusModHttpRepository] steam_app_id=%s domain=%s count=%s",
            steam_app_id,
            game_domain,
            len(mods),
        )
        return mods
