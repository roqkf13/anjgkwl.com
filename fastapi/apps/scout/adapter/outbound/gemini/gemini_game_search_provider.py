"""임의의 게임(Steam/모바일 불문)을 Gemini 웹검색 그라운딩으로 조사."""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time

from google.genai import types

from scout.app.ports.output.game_search_provider import GameSearchProvider
from scout.domain.entities.scout_search_entry_entity import ScoutSearchEntryEntity

logger = logging.getLogger(__name__)

_MAX_ATTEMPTS = 4
_MIN_INTERVAL_SEC = 5.0

_PROMPT_TEMPLATE = (
    "너는 게임 정보 조사원이다. 웹검색을 사용해 아래 게임에 대한 정보를 조사하고 "
    "JSON만 출력하라. Steam 게임이든 모바일 게임이든 상관없다.\n"
    "형식: {{\"title\":\"정식 제목\",\"platform\":\"steam|mobile|other\","
    "\"summary\":\"한국어 2문장 이내 요약\",\"official_site_url\":\"공식 사이트 또는 "
    "스토어 URL\",\"videos\":[{{\"title\":\"영상 제목\",\"channel\":\"채널명\","
    "\"published_at\":\"YYYY-MM-DD 또는 빈 문자열\",\"watch_url\":\"영상 URL\"}}]}}\n"
    "videos는 실존하는 트레일러/플레이 영상 2~4개로 채워라. 찾을 수 없으면 빈 배열로 둬라.\n"
    "게임: {query}"
)


def _parse_json_response(raw: str) -> dict:
    text = raw.strip()
    fenced = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.I)
    if fenced:
        text = fenced.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        raise ValueError("JSON not found")
    return json.loads(text[start : end + 1])


def _is_rate_limit(err: Exception) -> bool:
    m = str(err).lower()
    return "429" in m or "quota" in m


def _retry_delay(err: Exception) -> float:
    m = re.search(r"retry in ([\d.]+)s", str(err), re.I)
    return float(m.group(1)) + 2.0 if m else _MIN_INTERVAL_SEC


class GeminiGameSearchProvider(GameSearchProvider):
    async def search(self, query: str) -> ScoutSearchEntryEntity | None:
        from core.matrix.vault_keymaker_secret_manager import is_gemini_configured

        if not is_gemini_configured():
            logger.warning("[GeminiGameSearchProvider] GEMINI_API_KEY not configured")
            return None

        try:
            return await asyncio.to_thread(self._search_with_retry, query)
        except Exception as e:
            logger.warning("[GeminiGameSearchProvider] failed query=%s err=%s", query, e)
            return None

    def _search_with_retry(self, query: str) -> ScoutSearchEntryEntity | None:
        last: Exception | None = None
        for attempt in range(_MAX_ATTEMPTS):
            try:
                return self._search_once(query)
            except Exception as e:
                last = e
                if attempt >= _MAX_ATTEMPTS - 1 or not _is_rate_limit(e):
                    raise
                time.sleep(_retry_delay(e))
        raise last or RuntimeError("game search failed")

    def _search_once(self, query: str) -> ScoutSearchEntryEntity | None:
        from core.matrix.vault_keymaker_secret_manager import (
            get_gemini_client,
            get_gemini_model_name,
        )

        client = get_gemini_client()
        model_name = get_gemini_model_name()
        prompt = _PROMPT_TEMPLATE.format(query=query.strip())
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[types.Tool(google_search=types.GoogleSearch())]
            ),
        )
        raw = (response.text or "").strip()
        if not raw:
            return None

        data = _parse_json_response(raw)
        title = (data.get("title") or query).strip()
        videos = [
            {
                "title": (v.get("title") or "").strip(),
                "channel": (v.get("channel") or "").strip(),
                "watch_url": (v.get("watch_url") or "").strip(),
                "published_at": (v.get("published_at") or "").strip() or None,
            }
            for v in (data.get("videos") or [])
            if v.get("watch_url")
        ]

        return ScoutSearchEntryEntity(
            id=None,
            query_key="",
            title=title,
            platform=(data.get("platform") or "other").strip(),
            summary=(data.get("summary") or "").strip() or None,
            official_site_url=(data.get("official_site_url") or "").strip() or None,
            videos=videos,
        )
