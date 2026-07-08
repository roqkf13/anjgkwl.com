from functools import lru_cache

from sherlock_homes.adapter.outbound.repositories.kcelectra_content_moderation_repository import (
    KcElectraContentModerationRepository,
)
from sherlock_homes.app.ports.input.content_moderation_use_case import ContentModerationUseCase
from sherlock_homes.app.use_cases.content_moderation_interactor import ContentModerationInteractor


@lru_cache(maxsize=1)
def get_content_moderation_use_case() -> ContentModerationUseCase:
    return ContentModerationInteractor(model=KcElectraContentModerationRepository())
