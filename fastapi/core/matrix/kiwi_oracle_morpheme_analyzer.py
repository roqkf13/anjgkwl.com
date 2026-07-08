"""KiwiPy 형태소 분석기 — get_kiwi()로 싱글턴 인스턴스를 주입받는다."""

from functools import lru_cache

from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords


@lru_cache
def get_kiwi() -> Kiwi:
    return Kiwi()


@lru_cache
def get_stopwords() -> Stopwords:
    return Stopwords()


__all__ = ["get_kiwi", "get_stopwords"]
