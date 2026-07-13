from community.adapter.outbound.repositories.discord_repository import DiscordMemoryRepository
from community.app.ports.input.discord_use_case import DiscordUseCase
from community.app.use_cases.discord_interactor import DiscordInteractor


def get_discord_use_case() -> DiscordUseCase:
    return DiscordInteractor(repository=DiscordMemoryRepository())
