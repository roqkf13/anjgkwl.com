from community.adapter.outbound.repositories.telegram_repository import TelegramMemoryRepository
from community.app.ports.input.telegram_use_case import TelegramUseCase
from community.app.use_cases.telegram_interactor import TelegramInteractor


def get_telegram_use_case() -> TelegramUseCase:
    return TelegramInteractor(repository=TelegramMemoryRepository())
