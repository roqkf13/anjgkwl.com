from sherlock_homes.adapter.outbound.repositories.discord_repository import DiscordMemoryRepository
from sherlock_homes.app.ports.input.discord_use_case import DiscordUseCase
from sherlock_homes.app.use_cases.discord_interactor import DiscordInteractor


def get_discord_use_case() -> DiscordUseCase:
    return DiscordInteractor(repository=DiscordMemoryRepository())
