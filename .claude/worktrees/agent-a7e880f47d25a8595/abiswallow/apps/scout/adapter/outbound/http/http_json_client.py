"""urllib 기반 JSON HTTP 클라이언트 (Steam News 어댑터와 동일 스타일)."""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT_SEC = 20


def fetch_json(
    url: str,
    *,
    headers: dict[str, str] | None = None,
    timeout_sec: int = _DEFAULT_TIMEOUT_SEC,
) -> Any | None:
    req = urllib.request.Request(
        url,
        headers={"accept": "application/json", **(headers or {})},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as e:
        logger.warning("[fetch_json] request failed url=%s err=%s", url, e)
        return None
    except json.JSONDecodeError as e:
        logger.warning("[fetch_json] invalid json url=%s err=%s", url, e)
        return None


def build_url(base: str, params: dict[str, str | int]) -> str:
    query = urllib.parse.urlencode(params)
    return f"{base}?{query}"
