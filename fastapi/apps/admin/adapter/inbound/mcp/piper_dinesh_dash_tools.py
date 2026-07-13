from mcp.server.fastmcp import FastMCP

mcp = FastMCP("myself")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 대시보드 엔지니어 디네시입니다"
