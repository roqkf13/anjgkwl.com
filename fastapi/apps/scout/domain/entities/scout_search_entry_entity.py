from __future__ import annotations


class ScoutSearchEntryEntity:
    def __init__(
        self,
        id,
        query_key: str,
        title: str,
        platform,
        summary,
        official_site_url,
        videos: list[dict],
        created_at=None,
    ) -> None:
        self._id = id
        self._query_key = query_key
        self._title = title
        self._platform = platform
        self._summary = summary
        self._official_site_url = official_site_url
        self._videos = videos
        self._created_at = created_at

    @property
    def id(self): return self._id

    @property
    def query_key(self): return self._query_key

    @property
    def title(self): return self._title

    @property
    def platform(self): return self._platform

    @property
    def summary(self): return self._summary

    @property
    def official_site_url(self): return self._official_site_url

    @property
    def videos(self): return self._videos

    @property
    def created_at(self): return self._created_at

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ScoutSearchEntryEntity):
            return NotImplemented
        return self._query_key == other._query_key

    def __hash__(self) -> int:
        return hash(self._query_key)
