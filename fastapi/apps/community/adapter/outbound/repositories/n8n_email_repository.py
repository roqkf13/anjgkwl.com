import os

import httpx

from community.app.dtos.detective_watson_executor_dto import WatsonSendEmailQuery, WatsonSendEmailResult
from community.app.ports.output.detective_watson_executor_email_gateway_port import WatsonEmailGatewayPort


class N8nEmailRepository(WatsonEmailGatewayPort):

    def __init__(self) -> None:
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL", "")

    async def send_email(self, query: WatsonSendEmailQuery, subject: str, body: str) -> WatsonSendEmailResult:
        if not self.webhook_url:
            raise ValueError(".env에 N8N_WEBHOOK_URL이 설정되지 않았습니다.")

        payload = {
            "to": query.to,
            "subject": subject,
            "body": body,
            "from_account": query.from_account,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.webhook_url, json=payload, timeout=30)
            response.raise_for_status()

        return WatsonSendEmailResult(
            message="발송 완료",
            subject=subject,
            to=query.to,
        )
