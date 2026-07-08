"""Steam ISteamNews API에서 패치 노트 원문을 가져온다."""

from __future__ import annotations

import asyncio
import html
import json
import logging
import re
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

from scout.app.dtos.game_detail_dto import PatchContentBlockDto, PatchNoteDto
from scout.app.ports.output.steam_news_repository import SteamNewsRepository
from scout.domain.patch_note_format import blocks_to_plain_body

logger = logging.getLogger(__name__)

_STEAM_NEWS_URL = "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/"
_DEFAULT_COUNT = 15
_FETCH_TIMEOUT_SEC = 8
_STEAM_CLAN_CDN = "https://clan.fastly.steamstatic.com/images"


def _normalize_steam_image_url(url: str) -> str:
    u = re.sub(r"\[/img.*$", "", url.strip(), flags=re.I)
    if not u:
        return ""
    if u.startswith("{STEAM_CLAN_IMAGE}"):
        path = u.removeprefix("{STEAM_CLAN_IMAGE}").lstrip("/")
        return f"{_STEAM_CLAN_CDN}/{path}" if path else ""
    if u.startswith("//"):
        return f"https:{u}"
    if u.startswith(("http://", "https://")):
        return u
    if u.startswith("/"):
        return f"https://steamcdn-a.akamaihd.net{u}"
    return u


_IMAGE_SEGMENT = re.compile(
    r"<img[^>]*>|"
    r"\[img\][^\[]*\[/img\]|"
    r"\{STEAM_CLAN_IMAGE\}/[^\s\}\[\]<\"']+",
    re.I,
)


def _image_url_from_segment(segment: str) -> str:
    if segment.lower().startswith("<img"):
        m = re.search(r'src=["\']([^"\']+)["\']', segment, flags=re.I)
        return _normalize_steam_image_url(m.group(1)) if m else ""
    if segment.lower().startswith("[img"):
        m = re.search(r"\[img\]([^\[]+)\[/img\]", segment, flags=re.I | re.DOTALL)
        return _normalize_steam_image_url(m.group(1)) if m else ""
    return _normalize_steam_image_url(segment)


def parse_content_blocks(raw: str) -> list[PatchContentBlockDto]:
    """Steam 본문을 원문 순서의 텍스트·이미지 블록으로 분해한다."""
    if not raw:
        return []
    s = html.unescape(raw)
    blocks: list[PatchContentBlockDto] = []
    last = 0
    for m in _IMAGE_SEGMENT.finditer(s):
        if m.start() > last:
            text = bbcode_to_plain_text(s[last : m.start()])
            if text.strip():
                blocks.append(PatchContentBlockDto(type="text", text=text))
        url = _image_url_from_segment(m.group(0))
        if url:
            blocks.append(PatchContentBlockDto(type="image", url=url))
        last = m.end()
    if last < len(s):
        text = bbcode_to_plain_text(s[last:])
        if text.strip():
            blocks.append(PatchContentBlockDto(type="text", text=text))
    return blocks


def extract_image_urls(raw: str) -> list[str]:
    """Steam BBCode/HTML 본문에서 이미지 URL을 추출한다."""
    if not raw:
        return []
    s = html.unescape(raw)
    found: list[str] = []

    for m in re.finditer(r'<img[^>]+src=["\']([^"\']+)["\']', s, flags=re.I):
        found.append(_normalize_steam_image_url(m.group(1)))

    for m in re.finditer(r"\[img\]([^\[]+)\[/img\]", s, flags=re.I | re.DOTALL):
        found.append(_normalize_steam_image_url(m.group(1)))

    for m in re.finditer(r"\{STEAM_CLAN_IMAGE\}(/[^\s\}\[\]<\"']+)", s):
        found.append(f"{_STEAM_CLAN_CDN}{m.group(1)}")

    seen: set[str] = set()
    out: list[str] = []
    for u in found:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out


def bbcode_to_plain_text(raw: str) -> str:
    if not raw:
        return ""
    s = html.unescape(raw)
    s = re.sub(r"<script[^>]*>[\s\S]*?</script>", "", s, flags=re.I)
    s = re.sub(r"<style[^>]*>[\s\S]*?</style>", "", s, flags=re.I)
    s = re.sub(r"<img[^>]*>", "", s, flags=re.I)
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</p>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = re.sub(r"\[img\][^\[]*\[/img\]", "", s, flags=re.I | re.DOTALL)
    s = re.sub(r"\{STEAM_CLAN_IMAGE\}[^\]]*", "", s)
    for tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
        s = re.sub(rf"\[/?{tag}\]", "\n", s, flags=re.I)
    s = re.sub(r"\[/?b\]", "", s, flags=re.I)
    s = re.sub(r"\[/?i\]", "", s, flags=re.I)
    s = re.sub(r"\[/?u\]", "", s, flags=re.I)
    s = re.sub(r"\[/?list\]", "\n", s, flags=re.I)
    s = re.sub(r"\[\*\]", "· ", s)
    s = re.sub(r"\[url=([^\]]+)\]([^\[]*)\[/url\]", r"\2", s, flags=re.I)
    s = re.sub(r"\[url\]([^\[]*)\[/url\]", r"\1", s, flags=re.I)
    s = re.sub(r"\[/?quote\]", "\n", s, flags=re.I)
    s = re.sub(r"\[/?code\]", "", s, flags=re.I)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


class SteamNewsHttpRepository(SteamNewsRepository):
    async def fetch_patch_notes(
        self, steam_app_id: int, *, count: int = _DEFAULT_COUNT
    ) -> list[PatchNoteDto]:
        return await asyncio.to_thread(self._fetch_sync, steam_app_id, count)

    def _fetch_sync(self, steam_app_id: int, count: int) -> list[PatchNoteDto]:
        params = urllib.parse.urlencode(
            {"appid": steam_app_id, "count": count, "maxlength": 0}
        )
        url = f"{_STEAM_NEWS_URL}?{params}"
        try:
            with urllib.request.urlopen(url, timeout=_FETCH_TIMEOUT_SEC) as resp:
                payload = json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            logger.warning(
                "[SteamNewsHttpRepository] fetch failed steam_app_id=%s err=%s",
                steam_app_id,
                e,
            )
            return []

        items = (payload.get("appnews") or {}).get("newsitems") or []
        notes: list[PatchNoteDto] = []
        for item in items:
            url = (item.get("url") or "").lower()
            # 공식 패치 노트(Steam 커뮤니티 공지)만 — PCGamesN 등 외부 기사 제외
            if "steam_community_announcement" not in url:
                continue
            gid = str(item.get("gid") or "").strip()
            title = (item.get("title") or "").strip()
            raw_contents = (item.get("contents") or "").strip()
            content_blocks = parse_content_blocks(raw_contents)
            body = blocks_to_plain_body(content_blocks) or bbcode_to_plain_text(
                raw_contents
            )
            image_urls = [
                b.url for b in content_blocks if b.type == "image" and b.url
            ] or extract_image_urls(raw_contents)
            if not gid or not title or not body:
                continue
            published = datetime.fromtimestamp(
                int(item.get("date") or 0), tz=timezone.utc
            ).strftime("%Y-%m-%d")
            source = (item.get("url") or "").strip() or None
            notes.append(
                PatchNoteDto(
                    id=f"{steam_app_id}-steam-{gid}",
                    title=title,
                    published_at=published,
                    summary=body[:220] + ("…" if len(body) > 220 else ""),
                    body_ko=body,
                    image_urls=image_urls,
                    content_blocks=content_blocks,
                    source_url=source,
                )
            )
        return notes
