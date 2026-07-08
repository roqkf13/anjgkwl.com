from __future__ import annotations


class ScoutRelatedVideoEntity:
    def __init__(
        self,
        id,
        game_id: int,
        title: str,
        channel: str,
        published_at,
        watch_url: str,
    ) -> None:
        self._id = id
        self._game_id = game_id
        self._title = title
        self._channel = channel
        self._published_at = published_at
        self._watch_url = watch_url

    @property
    def id(self): return self._id

    @property
    def game_id(self): return self._game_id

    @property
    def title(self): return self._title

    @property
    def channel(self): return self._channel

    @property
    def published_at(self): return self._published_at

    @property
    def watch_url(self): return self._watch_url
