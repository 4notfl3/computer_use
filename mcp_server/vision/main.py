"""Vision MCP Server — 屏幕截图 + AI 图像分析"""

from __future__ import annotations

from fastmcp import FastMCP

from mcp_server.vision.manager import VisionManager
from mcp_server.vision.tools import register_tools

mcp = FastMCP("Vision-Server")
vision = VisionManager()
register_tools(mcp, vision)

if __name__ == "__main__":
    mcp.run(transport="stdio")
