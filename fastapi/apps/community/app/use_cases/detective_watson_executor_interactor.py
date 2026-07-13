from __future__ import annotations

import asyncio

from community.app.dtos.detective_watson_executor_dto import (
    WatsonExecutorQuery,
    WatsonExecutorResponse,
    WatsonSendEmailQuery,
    WatsonSendEmailResult,
)
from community.app.ports.input.detective_watson_executor_use_case import WatsonExecutorUseCase
from community.app.ports.output.detective_watson_executor_port import WatsonExecutorPort
from community.app.ports.output.detective_watson_executor_email_gateway_port import WatsonEmailGatewayPort
from core.lol.t1_mid_faker_orchestrator import generate_reply_exaone


class WatsonExecutorInteractor(WatsonExecutorUseCase):

    def __init__(self, repo: WatsonExecutorPort, email_gateway: WatsonEmailGatewayPort) -> None:
        self._repo = repo
        self._email_gateway = email_gateway

    async def introduce_myself(self, query: WatsonExecutorQuery) -> WatsonExecutorResponse:
        return await self._repo.introduce_myself(query)

    async def send_email(self, query: WatsonSendEmailQuery) -> WatsonSendEmailResult:
        system = (
            "당신은 이메일 작성 전문가입니다. "
            "사용자의 지시를 바탕으로 자연스러운 한국어 이메일을 작성하세요. "
            "반드시 다음 형식으로만 응답하세요:\n"
            "제목: <이메일 제목>\n"
            "본문: <이메일 본문>"
        )
        raw = await asyncio.to_thread(
            generate_reply_exaone,
            message=query.prompt,
            system=system,
        )

        subject, body = self._parse_subject_body(raw, query.prompt)
        return await self._email_gateway.send_email(query, subject=subject, body=body)

    @staticmethod
    def _parse_subject_body(raw: str, fallback_prompt: str) -> tuple[str, str]:
        subject = f"[왓슨] {fallback_prompt[:20]}"
        body = raw
        lines = raw.splitlines()
        body_start = None
        for i, line in enumerate(lines):
            if line.startswith("제목:"):
                subject = line.removeprefix("제목:").strip()
            elif line.startswith("본문:"):
                first_body_line = line.removeprefix("본문:").strip()
                rest = "\n".join(lines[i + 1:]).strip()
                body = f"{first_body_line}\n{rest}".strip() if rest else first_body_line
                body_start = i
                break
        return subject, body
