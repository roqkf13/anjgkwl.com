from __future__ import annotations

from scout.adapter.outbound.orm.scout_mod_orm import ScoutModOrm
from scout.adapter.outbound.orm.scout_mod_character_orm import ScoutModCharacterOrm
from scout.domain.entities.scout_mod_entity import ScoutModEntity
from scout.domain.value_objects.scout_mod_vo import ModKind, ModSource, CharacterSlug, ExternalModId


class ScoutModMapper:
    @staticmethod
    def to_entity(orm: ScoutModOrm, characters_list: list[ScoutModCharacterOrm]) -> ScoutModEntity:
        return ScoutModEntity(
            id=orm.id,
            game_id=orm.game_id,
            mod_kind=ModKind(orm.mod_kind),
            name=orm.name,
            author=orm.author,
            summary=orm.summary,
            characters=[CharacterSlug(c.character_slug) for c in characters_list],
            source=ModSource(orm.source) if orm.source else None,
            source_url=orm.source_url,
            external_mod_id=ExternalModId(orm.external_mod_id) if orm.external_mod_id else None,
        )

    @staticmethod
    def to_orm(entity: ScoutModEntity, game_id: int) -> ScoutModOrm:
        return ScoutModOrm(
            game_id=game_id,
            mod_kind=entity.mod_kind.value,
            name=entity.name,
            author=entity.author,
            summary=entity.summary,
            source=entity.source.value if entity.source else None,
            source_url=entity.source_url,
            external_mod_id=entity.external_mod_id.value if entity.external_mod_id else None,
        )

    @staticmethod
    def to_character_orms(entity: ScoutModEntity, mod_id: int) -> list[ScoutModCharacterOrm]:
        return [ScoutModCharacterOrm(mod_id=mod_id, character_slug=c.value) for c in entity.characters]
