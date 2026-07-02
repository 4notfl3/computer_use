"""Browser MCP Server — Playwright 驱动的浏览器自动化"""

from __future__ import annotations

from fastmcp import FastMCP

from mcp_server.browser.engine import BrowserManager
from mcp_server.browser.tools import register_tools

mcp = FastMCP("Browser-Server")
browser = BrowserManager()
register_tools(mcp, browser)

if __name__ == "__main__":
    mcp.run(transport="stdio")
