"""모드 목록 병합 시 중복 제거 키."""

from __future__ import annotations

import re
from urllib.parse import urlparse

from scout.app.dtos.game_detail_dto import ModDto

_NEXUS_MOD_ID_RE = re.compile(r"nexus-(\d+)(?:$|[^0-9])", re.I)
_NEXUS_MOD_URL_RE = re.compile(r"nexusmods\.com/[^/]+/mods/(\d+)", re.I)
_GITHUB_RELEASE_RE = re.compile(r"github\.com/([^/]+/[^/]+)/releases", re.I)
_PATREON_POST_RE = re.compile(r"patreon\.com/posts/([^/?#]+)", re.I)


def _nexus_mod_id(mod: ModDto) -> str | None:
    match = _NEXUS_MOD_ID_RE.search(mod.id)
    if match:
        return match.group(1)
    if mod.source_url:
        url_match = _NEXUS_MOD_URL_RE.search(mod.source_url)
        if url_match:
            return url_match.group(1)
    return None


def mod_dedupe_key(mod: ModDto) -> str:
    """같은 배포 페이지·Nexus 모드는 하나로 묶는다."""
    nexus_id = _nexus_mod_id(mod)
    if nexus_id:
        return f"nexus:{nexus_id}"

    url = (mod.source_url or "").strip()
    if url:
        github_match = _GITHUB_RELEASE_RE.search(url)
        if github_match:
            return f"github:{github_match.group(1).lower()}"

        patreon_match = _PATREON_POST_RE.search(url)
        if patreon_match:
            return f"patreon:{patreon_match.group(1).lower()}"

        parsed = urlparse(url.lower().rstrip("/"))
        if parsed.netloc:
            if parsed.query:
                return f"url:{parsed.netloc}{parsed.path}?{parsed.query}"
            return f"url:{parsed.netloc}{parsed.path}"

    return f"id:{mod.id.strip().lower()}"
