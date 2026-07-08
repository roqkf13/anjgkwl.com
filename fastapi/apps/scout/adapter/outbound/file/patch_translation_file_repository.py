"""패치 노트 한글 번역 결과를 디스크에 보관."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path

from scout.app.dtos.game_detail_dto import PatchNoteDto
from scout.domain.patch_note_rules import is_korean_translation
from scout.app.ports.output.patch_translation_repository import (
    PatchTranslationRepository,
)

logger = logging.getLogger(__name__)

_CACHE_DIR = Path(__file__).resolve().parents[3] / "data" / "patch_translations"


def _safe_name(note_id: str) -> str:
    return re.sub(r"[^\w.-]", "_", note_id)


def _path(note_id: str) -> Path:
    _CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return _CACHE_DIR / f"{_safe_name(note_id)}.json"


class PatchTranslationFileRepository(PatchTranslationRepository):
    def load(self, note_id: str) -> PatchNoteDto | None:
        path = _path(note_id)
        if not path.is_file():
            return None
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            note = PatchNoteDto.model_validate(data)
            if is_korean_translation(note):
                return note
        except (json.JSONDecodeError, OSError, ValueError) as e:
            logger.warning(
                "[PatchTranslationFileRepository] load failed id=%s err=%s",
                note_id,
                e,
            )
        return None

    def save(self, note: PatchNoteDto) -> None:
        if not is_korean_translation(note):
            return
        try:
            _path(note.id).write_text(
                json.dumps(note.model_dump(mode="json"), ensure_ascii=False, indent=0),
                encoding="utf-8",
            )
        except OSError as e:
            logger.warning(
                "[PatchTranslationFileRepository] save failed id=%s err=%s",
                note.id,
                e,
            )
