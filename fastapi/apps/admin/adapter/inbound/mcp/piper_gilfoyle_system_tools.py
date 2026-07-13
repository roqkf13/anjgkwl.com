from mcp.server.fastmcp import FastMCP

mcp = FastMCP("myself")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 시스템 아키텍트 길포일입니다"
