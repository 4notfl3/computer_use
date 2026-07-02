"""Browser MCP 工具注册 — 将 engine 方法暴露为 MCP tools"""

from __future__ import annotations

from fastmcp import FastMCP

from mcp_server.browser.engine import BrowserManager


def register_tools(mcp: FastMCP, browser: BrowserManager) -> None:
    """将 browser 的四个操作注册为 MCP 工具"""

    @mcp.tool()
    async def browser_navigate(url: str) -> str:
        """打开或跳转到指定网址"""
        return await browser.navigate(url)

    @mcp.tool()
    async def browser_click(selector: str) -> str:
        """点击页面元素（支持 CSS 选择器，如 'button', '#submit', '.class'）"""
        return await browser.click(selector)

    @mcp.tool()
    async def browser_fill(selector: str, text: str) -> str:
        """在输入框输入内容"""
        return await browser.fill(selector, text)

    @mcp.tool()
    async def browser_read_content() -> str:
        """读取当前页面的主要文本内容"""
        return await browser.get_content()
