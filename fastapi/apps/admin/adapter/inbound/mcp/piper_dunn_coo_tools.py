# apps/admin/adapter/inbound/mcp/piper_dunn_coo_tools.py
from mcp.server.fastmcp import FastMCP
from apps.admin.adapter.outbound.client.n8n_client import N8nClient

# 1. MCP 서버 초기화
mcp = FastMCP("myself")

@mcp.tool()
async def introduce_myself() -> str:
    """파이퍼 COO 자신을 소개하고 n8n 알림을 보냅니다."""
    
    # 2. n8n 아웃바운드 클라이언트 생성
    n8n = N8nClient()
    
    try:
        # 3. 반드시 'async def' 함수 내부에서 await를 사용해야 합니다!
        await n8n.send_slack_notification("👔 파이퍼 던 COO의 introduce_myself 툴이 실행되었습니다!")
    except Exception as e:
        # 알림 전송에 실패해도 툴 기능 자체가 죽지 않도록 안전장치 마련
        print(f"슬랙 알림 전송 실패: {e}")

    return "파이퍼 COO 던입니다"

# 파일 맨 밑에 직접 실행용 테스트 코드 추가
if __name__ == "__main__":
    import asyncio
    from dotenv import load_dotenv
    load_dotenv() # .env 웹훅 주소 읽기

    async def test_call():
        print("🎯 파이퍼 던 COO 툴 직접 호출 시작...")
        # 함수를 직접 실행해봅니다.
        result = await introduce_myself()
        print(f"🤖 툴 반환 결과: {result}")

    asyncio.run(test_call())