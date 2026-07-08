from __future__ import annotations

from scout.adapter.outbound.orm.scout_genre_orm import ScoutGenreOrm
from scout.adapter.outbound.orm.scout_genre_trait_orm import ScoutGenreTraitOrm
from scout.domain.entities.scout_genre_entity import ScoutGenreEntity
from scout.domain.value_objects.scout_genre_vo import GenreSlug, GenreLabel


class ScoutGenreMapper:
    @staticmethod
    def to_entity(orm: ScoutGenreOrm, traits_list: list[ScoutGenreTraitOrm]) -> ScoutGenreEntity:
        return ScoutGenreEntity(
            id=orm.id,
            slug=GenreSlug(orm.slug),
            label=GenreLabel(orm.label),
            description=orm.description or "",
            traits=[t.trait for t in traits_list],
            representative_game_id=orm.representative_game_id,
        )

    @staticmethod
    def to_orm(entity: ScoutGenreEntity) -> ScoutGenreOrm:
        return ScoutGenreOrm(
            slug=entity.slug.value,
            label=entity.label.value,
            description=entity.description,
            representative_game_id=entity.representative_game_id,
        )

    @staticmethod
    def to_trait_orms(entity: ScoutGenreEntity, genre_id: int) -> list[ScoutGenreTraitOrm]:
        return [ScoutGenreTraitOrm(genre_id=genre_id, trait=t) for t in entity.traits]
