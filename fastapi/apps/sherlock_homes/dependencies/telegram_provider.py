from sherlock_homes.adapter.outbound.repositories.telegram_repository import TelegramMemoryRepository
from sherlock_homes.app.ports.input.telegram_use_case import TelegramUseCase
from sherlock_homes.app.use_cases.telegram_interactor import TelegramInteractor


def get_telegram_use_case() -> TelegramUseCase:
    return TelegramInteractor(repository=TelegramMemoryRepository())
