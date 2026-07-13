from functools import lru_cache

from community.adapter.outbound.repositories.n8n_email_repository import N8nEmailRepository
from community.adapter.outbound.repositories.watson_memory_repository import WatsonMemoryRepository
from community.app.use_cases.detective_watson_executor_interactor import WatsonExecutorInteractor


@lru_cache(maxsize=1)
def get_watson_executor_interactor() -> WatsonExecutorInteractor:
    return WatsonExecutorInteractor(
        repo=WatsonMemoryRepository(),
        email_gateway=N8nEmailRepository(),
    )
