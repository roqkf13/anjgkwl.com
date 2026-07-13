from __future__ import annotations

from scout.adapter.outbound.orm.scout_search_entry_orm import ScoutSearchEntryOrm
from scout.domain.entities.scout_search_entry_entity import ScoutSearchEntryEntity


class ScoutSearchEntryMapper:
    @staticmethod
    def to_entity(orm: ScoutSearchEntryOrm) -> ScoutSearchEntryEntity:
        return ScoutSearchEntryEntity(
            id=orm.id,
            query_key=orm.query_key,
            title=orm.title,
            platform=orm.platform,
            summary=orm.summary,
            official_site_url=orm.official_site_url,
            videos=orm.videos or [],
            created_at=orm.created_at,
        )

    @staticmethod
    def to_orm(entity: ScoutSearchEntryEntity) -> ScoutSearchEntryOrm:
        return ScoutSearchEntryOrm(
            query_key=entity.query_key,
            title=entity.title,
            platform=entity.platform,
            summary=entity.summary,
            official_site_url=entity.official_site_url,
            videos=entity.videos,
        )
