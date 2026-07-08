from __future__ import annotations

from scout.adapter.outbound.orm.scout_game_orm import ScoutGameOrm
from scout.domain.entities.scout_game_entity import ScoutGameEntity
from scout.domain.value_objects.scout_game_vo import SteamAppId, GameTitle


class ScoutGameMapper:
    @staticmethod
    def to_entity(orm: ScoutGameOrm) -> ScoutGameEntity:
        return ScoutGameEntity(
            id=orm.id,
            steam_app_id=SteamAppId(orm.steam_app_id),
            title=GameTitle(orm.title),
            summary=orm.summary,
            genre_id=orm.genre_id,
            official_site_url=orm.official_site_url,
        )

    @staticmethod
    def to_orm(entity: ScoutGameEntity) -> ScoutGameOrm:
        return ScoutGameOrm(
            steam_app_id=entity.steam_app_id.value,
            genre_id=entity.genre_id,
            title=entity.title.value,
            summary=entity.summary,
            official_site_url=entity.official_site_url,
        )
