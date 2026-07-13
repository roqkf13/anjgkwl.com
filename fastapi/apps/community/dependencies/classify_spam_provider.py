from community.adapter.outbound.repositories.exaone_classify_spam_repository import ExaoneClassifySpamRepository
from community.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from community.app.use_cases.classify_spam_interactor import ClassifySpamInteractor


def get_classify_spam_use_case() -> ClassifySpamUseCase:
    return ClassifySpamInteractor(llm_gateway=ExaoneClassifySpamRepository())
