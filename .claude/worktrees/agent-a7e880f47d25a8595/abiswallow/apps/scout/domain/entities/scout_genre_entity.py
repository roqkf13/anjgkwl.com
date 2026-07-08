from __future__ import annotations

from scout.domain.value_objects.scout_genre_vo import GenreSlug, GenreLabel


class ScoutGenreEntity:
    def __init__(
        self,
        id,
        slug: GenreSlug,
        label: GenreLabel,
        description: str,
        traits: list[str],
        representative_game_id=None,
    ) -> None:
        self._id = id
        self._slug = slug
        self._label = label
        self._description = description
        self._traits = traits
        self._representative_game_id = representative_game_id

    @property
    def id(self): return self._id

    @property
    def slug(self): return self._slug

    @property
    def label(self): return self._label

    @property
    def description(self): return self._description

    @property
    def traits(self): return list(self._traits)

    @property
    def representative_game_id(self): return self._representative_game_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScoutGenreEntity):
            return NotImplemented
        return self._slug == other._slug

    def __hash__(self) -> int:
        return hash(self._slug)
