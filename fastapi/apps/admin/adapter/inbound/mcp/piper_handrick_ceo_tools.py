from mcp.server.fastmcp import FastMCP

mcp = FastMCP("myself")

@mcp.tool()
async def introduce_myself() -> str:
    return "파이퍼 CEO 핸드릭스입니다"
