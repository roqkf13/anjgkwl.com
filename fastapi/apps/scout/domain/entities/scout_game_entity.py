from __future__ import annotations

from scout.domain.value_objects.scout_game_vo import SteamAppId, GameTitle


class ScoutGameEntity:
    def __init__(
        self,
        id,
        steam_app_id: SteamAppId,
        title: GameTitle,
        summary,
        genre_id,
        official_site_url=None,
    ) -> None:
        self._id = id
        self._steam_app_id = steam_app_id
        self._title = title
        self._summary = summary
        self._genre_id = genre_id
        self._official_site_url = official_site_url

    @property
    def id(self): return self._id

    @property
    def steam_app_id(self): return self._steam_app_id

    @property
    def title(self): return self._title

    @property
    def summary(self): return self._summary

    @property
    def genre_id(self): return self._genre_id

    @property
    def official_site_url(self): return self._official_site_url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScoutGameEntity):
            return NotImplemented
        return self._steam_app_id == other._steam_app_id

    def __hash__(self) -> int:
        return hash(self._steam_app_id)
