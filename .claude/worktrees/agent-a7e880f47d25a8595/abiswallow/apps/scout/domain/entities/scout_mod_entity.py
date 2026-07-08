from __future__ import annotations

from scout.domain.value_objects.scout_mod_vo import ModKind, ModSource, CharacterSlug, ExternalModId


class ScoutModEntity:
    def __init__(
        self,
        id,
        game_id: int,
        mod_kind: ModKind,
        name: str,
        author: str,
        summary,
        characters: list[CharacterSlug],
        source: ModSource | None,
        source_url,
        external_mod_id: ExternalModId | None,
    ) -> None:
        self._id = id
        self._game_id = game_id
        self._mod_kind = mod_kind
        self._name = name
        self._author = author
        self._summary = summary
        self._characters = characters
        self._source = source
        self._source_url = source_url
        self._external_mod_id = external_mod_id

    @property
    def id(self): return self._id

    @property
    def game_id(self): return self._game_id

    @property
    def mod_kind(self): return self._mod_kind

    @property
    def name(self): return self._name

    @property
    def author(self): return self._author

    @property
    def summary(self): return self._summary

    @property
    def characters(self): return list(self._characters)

    @property
    def source(self): return self._source

    @property
    def source_url(self): return self._source_url

    @property
    def external_mod_id(self): return self._external_mod_id

    def is_appearance(self) -> bool:
        return self._mod_kind == ModKind.APPEARANCE

    def is_functional(self) -> bool:
        return self._mod_kind == ModKind.FUNCTIONAL
