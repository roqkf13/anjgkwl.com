from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from scout.domain.value_objects.scout_patch_note_vo import Locale, BlockType


@dataclass(frozen=True, slots=True)
class ContentBlock:
    block_type: BlockType
    text: str | None
    url: str | None


class ScoutPatchTranslationEntity:
    def __init__(
        self,
        id,
        patch_note_id: int,
        locale: Locale,
        translated_title,
        translated_summary,
        translated_body,
        image_urls: list[str],
        content_blocks: list[ContentBlock],
        translated_at,
    ) -> None:
        self._id = id
        self._patch_note_id = patch_note_id
        self._locale = locale
        self._translated_title = translated_title
        self._translated_summary = translated_summary
        self._translated_body = translated_body
        self._image_urls = image_urls
        self._content_blocks = content_blocks
        self._translated_at = translated_at

    @property
    def id(self): return self._id

    @property
    def patch_note_id(self): return self._patch_note_id

    @property
    def locale(self): return self._locale

    @property
    def translated_title(self): return self._translated_title

    @property
    def translated_summary(self): return self._translated_summary

    @property
    def translated_body(self): return self._translated_body

    @property
    def image_urls(self): return list(self._image_urls)

    @property
    def content_blocks(self): return list(self._content_blocks)

    @property
    def translated_at(self): return self._translated_at
