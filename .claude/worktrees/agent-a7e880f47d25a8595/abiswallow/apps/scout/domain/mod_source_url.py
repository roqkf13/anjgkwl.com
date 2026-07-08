"""모드 DTO에 source_url 이 없을 때 출처별 기본 링크를 보강한다."""

from __future__ import annotations

import re
import urllib.parse

from scout.app.dtos.game_detail_dto import ModDto

_NEXUS_MOD_ID_RE = re.compile(r"-nexus-(\d+)$")
_WORKSHOP_FILE_ID_RE = re.compile(r"-workshop-(\d+)$")

_PATREON_CREATOR = "https://www.patreon.com/cw/anaertailin/posts"


def _nexus_search_url(game_domain: str, query: str) -> str:
    params = urllib.parse.urlencode({"keyword": query})
    return f"https://www.nexusmods.com/{game_domain}/mods/?{params}"


def resolve_mod_source_url(
    mod: ModDto,
    *,
    nexus_game_domain: str | None = None,
) -> ModDto:
    if mod.source_url:
        return mod

    nexus_match = _NEXUS_MOD_ID_RE.search(mod.id)
    if nexus_match and nexus_game_domain:
        return mod.model_copy(
            update={
                "source_url": (
                    f"https://www.nexusmods.com/{nexus_game_domain}"
                    f"/mods/{nexus_match.group(1)}"
                )
            }
        )

    workshop_match = _WORKSHOP_FILE_ID_RE.search(mod.id)
    if workshop_match:
        file_id = workshop_match.group(1)
        return mod.model_copy(
            update={
                "source_url": (
                    "https://steamcommunity.com/sharedfiles/filedetails/"
                    f"?id={file_id}"
                )
            }
        )

    source = mod.source
    if source == "github":
        return mod.model_copy(
            update={
                "source_url": _github_search_url(mod.name, mod.author),
            }
        )
    if source == "curated" and mod.author.lower() == "anaertailin":
        return mod.model_copy(update={"source_url": _PATREON_CREATOR})
    if source == "nexus" and nexus_game_domain:
        return mod.model_copy(
            update={
                "source_url": _nexus_search_url(nexus_game_domain, mod.name),
            }
        )

    return mod


def _github_search_url(name: str, author: str) -> str:
    query = urllib.parse.quote(f"{name} {author} slay the spire 2")
    return f"https://github.com/search?q={query}&type=repositories"
