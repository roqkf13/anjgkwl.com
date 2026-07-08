"""Steam Workshop(IPublishedFileService)에서 게임별 모드를 가져온다."""

from __future__ import annotations

import asyncio
import logging
import os
import re
from typing import Any

from scout.adapter.outbound.http.http_json_client import build_url, fetch_json
from scout.app.dtos.game_detail_dto import ModDto
from scout.domain.mod_character_rules import infer_mod_characters
from scout.domain.mod_kind_rules import classify_mod_kind

logger = logging.getLogger(__name__)

_WORKSHOP_QUERY_URL = (
    "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"
)
_DEFAULT_LIMIT = 10
_SUMMARY_MAX = 280
# EPublishedFileQueryType: 3 = RankedByTrend
_QUERY_TYPE_TRENDING = 3


def _steam_api_key() -> str:
    return os.getenv("STEAM_API_KEY", "").strip()


def _plain_text(raw: str) -> str:
    if not raw:
        return ""
    text = re.sub(r"<[^>]+>", " ", raw)
    text = re.sub(r"\[/?[^\]]+\]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _tag_names(item: dict[str, Any]) -> list[str]:
    tags = item.get("tags")
    if not isinstance(tags, list):
        return []
    names: list[str] = []
    for tag in tags:
        if isinstance(tag, dict):
            name = (tag.get("tag") or "").strip()
            if name:
                names.append(name)
        elif isinstance(tag, str) and tag.strip():
            names.append(tag.strip())
    return names


def _parse_workshop_items(payload: Any) -> list[dict[str, Any]]:
    if not isinstance(payload, dict):
        return []
    response = payload.get("response")
    if not isinstance(response, dict):
        return []
    items = response.get("publishedfiledetails")
    if not isinstance(items, list):
        return []
    return [item for item in items if isinstance(item, dict)]


def _to_mod_dto(*, steam_app_id: int, item: dict[str, Any]) -> ModDto | None:
    file_id = item.get("publishedfileid")
    title = (item.get("title") or "").strip()
    if file_id is None or not title:
        return None
    file_id_str = str(file_id).strip()
    description = _plain_text((item.get("description") or "").strip())
    if not description:
        description = "Steam Workshop 모드입니다."
    if len(description) > _SUMMARY_MAX:
        description = description[: _SUMMARY_MAX - 1] + "…"
    tags = _tag_names(item)
    creator = (item.get("creator") or "").strip()
    author = f"Steam Workshop · {creator}" if creator else "Steam Workshop"
    return ModDto(
        id=f"{steam_app_id}-workshop-{file_id_str}",
        mod_kind=classify_mod_kind(title, description, tags=tags),
        name=title,
        author=author,
        summary=description,
        characters=infer_mod_characters(title, description, tags=tags),
        source="workshop",
        source_url=(
            "https://steamcommunity.com/sharedfiles/filedetails/"
            f"?id={file_id_str}"
        ),
    )


class WorkshopModHttpRepository:
    async def fetch_mods(
        self, steam_app_id: int, *, limit: int = _DEFAULT_LIMIT
    ) -> list[ModDto]:
        return await asyncio.to_thread(self._fetch_sync, steam_app_id, limit)

    def _fetch_sync(self, steam_app_id: int, limit: int) -> list[ModDto]:
        api_key = _steam_api_key()
        if not api_key:
            logger.info(
                "[WorkshopModHttpRepository] skip steam_app_id=%s "
                "(STEAM_API_KEY missing)",
                steam_app_id,
            )
            return []

        url = build_url(
            _WORKSHOP_QUERY_URL,
            {
                "key": api_key,
                "appid": steam_app_id,
                "creator_appid": steam_app_id,
                "query_type": _QUERY_TYPE_TRENDING,
                "numperpage": limit,
                "cursor": "*",
                "return_tags": "true",
                "filetype": 0,
            },
        )
        payload = fetch_json(url)
        if payload is None:
            return []

        mods: list[ModDto] = []
        for item in _parse_workshop_items(payload)[:limit]:
            dto = _to_mod_dto(steam_app_id=steam_app_id, item=item)
            if dto:
                mods.append(dto)

        logger.info(
            "[WorkshopModHttpRepository] steam_app_id=%s count=%s",
            steam_app_id,
            len(mods),
        )
        return mods
