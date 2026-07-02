"""browser — 浏览器自动化 MCP Server

使用 Playwright 驱动本地 Edge 浏览器，支持页面导航、点击、
文本输入和内容读取等操作。
"""

from __future__ import annotations

from mcp_server.browser.engine import BrowserManager

__all__ = ["BrowserManager"]
