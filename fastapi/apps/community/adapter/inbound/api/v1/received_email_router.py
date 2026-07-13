from fastapi import APIRouter, Depends, HTTPException

from community.adapter.inbound.api.schemas.received_email_schema import (
    ReceiveEmailRequest,
    ReceivedEmailListSchema,
    ReceivedEmailSchema,
)
from community.app.dtos.content_moderation_dto import ContentModerationQuery
from community.app.dtos.received_email_dto import ReceivedEmailCommand
from community.app.ports.input.content_moderation_use_case import ContentModerationUseCase
from community.app.ports.input.received_email_use_case import ReceivedEmailUseCase
from community.dependencies.content_moderation_provider import get_content_moderation_use_case
from community.dependencies.received_email_provider import get_received_email_interactor

received_email_router = APIRouter(prefix="/watson", tags=["watson"])


@received_email_router.post("/emails/receive", response_model=ReceivedEmailSchema, summary="Gmail 수신 메일 저장")
async def receive_email(
    body: ReceiveEmailRequest,
    use_case: ReceivedEmailUseCase = Depends(get_received_email_interactor),
    moderation: ContentModerationUseCase = Depends(get_content_moderation_use_case),
) -> ReceivedEmailSchema:
    moderation_result = await moderation.moderate(
        ContentModerationQuery(subject=body.subject, body=body.snippet)
    )
    if not moderation_result.is_clean:
        raise HTTPException(
            status_code=422,
            detail=f"콘텐츠 필터링됨: {moderation_result.label} ({moderation_result.score:.2f})",
        )

    command = ReceivedEmailCommand(
        gmail_id=body.gmail_id,
        thread_id=body.thread_id,
        from_=body.from_,
        to=body.to,
        subject=body.subject,
        snippet=body.snippet,
    )
    result = await use_case.receive(command)
    return ReceivedEmailSchema(
        id=result.id,
        gmail_id=result.gmail_id,
        thread_id=result.thread_id,
        from_=result.from_,
        to=result.to,
        subject=result.subject,
        snippet=result.snippet,
    )


@received_email_router.get("/emails", response_model=ReceivedEmailListSchema, summary="수신 메일 목록 조회")
async def list_emails(
    use_case: ReceivedEmailUseCase = Depends(get_received_email_interactor),
) -> ReceivedEmailListSchema:
    result = await use_case.list_all()
    return ReceivedEmailListSchema(
        total=result.total,
        emails=[
            ReceivedEmailSchema(
                id=e.id,
                gmail_id=e.gmail_id,
                thread_id=e.thread_id,
                from_=e.from_,
                to=e.to,
                subject=e.subject,
                snippet=e.snippet,
            )
            for e in result.emails
        ],
    )
