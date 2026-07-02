"""All-in-One MCP Server — 一键启动所有工具

将 browser + vision 的所有工具注册到一个 FastMCP 实例中。
推荐终端使用此入口，一个进程即可获得全部能力。

用法:
    uv run python -m mcp_server.combined
"""

from __future__ import annotations

from fastmcp import FastMCP

from mcp_server.browser.engine import BrowserManager
from mcp_server.browser.tools import register_tools as register_browser
from mcp_server.vision.manager import VisionManager
from mcp_server.vision.tools import register_tools as register_vision

mcp = FastMCP("Computer-Use")

browser = BrowserManager()
register_browser(mcp, browser)

vision = VisionManager()
register_vision(mcp, vision)

if __name__ == "__main__":
    mcp.run(transport="stdio")
