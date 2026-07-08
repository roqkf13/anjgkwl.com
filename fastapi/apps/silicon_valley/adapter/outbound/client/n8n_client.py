# apps/silicon_valley/adapter/outbound/client/n8n_client.py
import httpx
import os

class N8nClient:
    def __init__(self):
        # .env 파일에 등록한 N8N_WEBHOOK_URL을 가져옵니다.
        # 만약 로컬 환경 변수 테스트라면 os.getenv를 사용하고, 
        # 프로젝트 자체 config 클래스가 있다면 그걸 활용하셔도 됩니다.
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL")

    async def send_slack_notification(self, message: str) -> dict:
        """n8n Webhook으로 POST 요청을 보내 슬랙 메시지를 트리거합니다."""
        if not self.webhook_url:
            raise ValueError(".env 파일에 N8N_WEBHOOK_URL이 설정되지 않았습니다.")

        # n8n으로 보낼 보따리(JSON 데이터)를 조립합니다.
        payload = {
            "message_text": message
        }

        # 비동기 HTTP 클라이언트를 열어 POST로 데이터를 쏩니다.
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.webhook_url, json=payload)
                response.raise_for_status()  # 에러 발생 시 예외 발생
                return response.json()       # n8n이 돌려준 결과 반환
            except httpx.HTTPStatusError as e:
                print(f"n8n 서버 에러 발생: {e.response.status_code}")
                raise e


# 파일 맨 밑에 추가할 테스트 실행 코드
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv

    # .env 파일의 환경변수(N8N_WEBHOOK_URL)를 로드합니다.
    load_dotenv()

    async def test_run():
        print("🚀 n8n 아웃바운드 직접 테스트 시작...")
        client = N8nClient()
        try:
            result = await client.send_slack_notification("FastAPI 아웃바운드 클래스 단독 테스트 성공! 🎯")
            print("✅ 전송 성공! n8n 응답:", result)
        except Exception as e:
            print("❌ 전송 실패 사유:", str(e))

    asyncio.run(test_run())                