from fastapi import APIRouter, Depends

from sherlock_homes.adapter.inbound.api.schemas.classify_spam_schema import (
    ClassifySpamRequest,
    ClassifySpamResponseSchema,
)
from sherlock_homes.app.dtos.classify_spam_dto import ClassifySpamQuery
from sherlock_homes.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from sherlock_homes.dependencies.classify_spam_provider import get_classify_spam_use_case

classify_spam_router = APIRouter(prefix="/spam", tags=["spam"])


@classify_spam_router.post("/classify", response_model=ClassifySpamResponseSchema, summary="이메일 스팸 카테고리 분류")
async def classify(
    schema: ClassifySpamRequest,
    use_case: ClassifySpamUseCase = Depends(get_classify_spam_use_case),
) -> ClassifySpamResponseSchema:
    query = ClassifySpamQuery(subject=schema.subject, body=schema.body)
    result = await use_case.classify(query)
    return ClassifySpamResponseSchema(category=result.category.value, reason=result.reason)
