from __future__ import annotations

from scout.domain.value_objects.scout_patch_note_vo import ExternalNoteId


class ScoutPatchNoteEntity:
    def __init__(
        self,
        id,
        game_id: int,
        external_note_id: ExternalNoteId,
        source_title: str,
        source_summary,
        source_body,
        image_urls: list[str],
        published_at,
        source_url,
    ) -> None:
        self._id = id
        self._game_id = game_id
        self._external_note_id = external_note_id
        self._source_title = source_title
        self._source_summary = source_summary
        self._source_body = source_body
        self._image_urls = image_urls
        self._published_at = published_at
        self._source_url = source_url

    @property
    def id(self): return self._id

    @property
    def game_id(self): return self._game_id

    @property
    def external_note_id(self): return self._external_note_id

    @property
    def source_title(self): return self._source_title

    @property
    def source_summary(self): return self._source_summary

    @property
    def source_body(self): return self._source_body

    @property
    def image_urls(self): return list(self._image_urls)

    @property
    def published_at(self): return self._published_at

    @property
    def source_url(self): return self._source_url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScoutPatchNoteEntity):
            return NotImplemented
        return self._external_note_id == other._external_note_id

    def __hash__(self) -> int:
        return hash(self._external_note_id)
