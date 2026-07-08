from sherlock_homes.adapter.outbound.repositories.exaone_classify_spam_repository import ExaoneClassifySpamRepository
from sherlock_homes.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from sherlock_homes.app.use_cases.classify_spam_interactor import ClassifySpamInteractor


def get_classify_spam_use_case() -> ClassifySpamUseCase:
    return ClassifySpamInteractor(llm_gateway=ExaoneClassifySpamRepository())
