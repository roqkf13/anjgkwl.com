"""장르 허브 — composition root (DIP)."""

from scout.adapter.outbound.static.metroidvania_static_repository import (
    MetroidvaniaStaticRepository,
)
from scout.adapter.outbound.static.openworld_static_repository import (
    OpenworldStaticRepository,
)
from scout.adapter.outbound.static.roguelike_static_repository import (
    RoguelikeStaticRepository,
)
from scout.adapter.outbound.static.soulslike_static_repository import (
    SoulslikeStaticRepository,
)
from scout.app.ports.input.genre_hub_use_case import GenreHubUseCase
from scout.app.ports.output.genre_hub_repository import GenreHubRepository
from scout.app.use_cases.metroidvania_interactor import MetroidvaniaInteractor
from scout.app.use_cases.openworld_interactor import OpenworldInteractor
from scout.app.use_cases.roguelike_interactor import RoguelikeInteractor
from scout.app.use_cases.soulslike_interactor import SoulslikeInteractor


def get_roguelike_use_case() -> GenreHubUseCase:
    repository: GenreHubRepository = RoguelikeStaticRepository()
    return RoguelikeInteractor(repository)


def get_soulslike_use_case() -> GenreHubUseCase:
    repository: GenreHubRepository = SoulslikeStaticRepository()
    return SoulslikeInteractor(repository)


def get_openworld_use_case() -> GenreHubUseCase:
    repository: GenreHubRepository = OpenworldStaticRepository()
    return OpenworldInteractor(repository)


def get_metroidvania_use_case() -> GenreHubUseCase:
    repository: GenreHubRepository = MetroidvaniaStaticRepository()
    return MetroidvaniaInteractor(repository)
