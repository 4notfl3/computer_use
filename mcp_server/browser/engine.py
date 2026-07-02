"""BrowserManager — Playwright 驱动的浏览器自动化引擎

纯业务逻辑，零 MCP 框架依赖，可独立测试。
"""

from __future__ import annotations

import os
from typing import Any

from playwright.async_api import async_playwright
from playwright.async_api._generated import Browser, BrowserContext, Page, Playwright

from shared.config import BROWSER_CHANNEL, BROWSER_HEADLESS, WORKSPACE_DIR


class BrowserError(Exception):
    """浏览器操作异常"""


class BrowserManager:
    """管理 Playwright 浏览器实例的生命周期和操作。

    支持延迟初始化：首次调用工具时自动启动浏览器。
    使用 async context manager 或手动调用 close() 释放资源。
    """

    def __init__(
        self,
        *,
        channel: str = BROWSER_CHANNEL,
        headless: bool = BROWSER_HEADLESS,
        user_data_dir: str | None = None,
    ) -> None:
        self._channel = channel
        self._headless = headless
        self._user_data_dir = user_data_dir or os.path.join(
            WORKSPACE_DIR, "browser_profile"
        )

        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self._page: Page | None = None

    # -- 生命周期 --

    async def __aenter__(self) -> "BrowserManager":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    async def ensure_browser(self) -> None:
        """确保浏览器已启动；若未启动则自动启动。"""
        if self._playwright is None:
            self._playwright = await async_playwright().start()

        if self._context is not None and self._context.is_closed():
            self._context = None
            self._page = None

        if self._context is None:
            os.makedirs(self._user_data_dir, exist_ok=True)
            self._browser = await self._playwright.chromium.launch(
                channel=self._channel,
                headless=self._headless,
            )
            self._context = await self._browser.new_context()
            self._page = await self._context.new_page()

    async def close(self) -> None:
        """释放所有浏览器资源。"""
        if self._context is not None:
            try:
                await self._context.close()
            except Exception:
                pass
            self._context = None
            self._page = None

        if self._browser is not None:
            try:
                await self._browser.close()
            except Exception:
                pass
            self._browser = None

        if self._playwright is not None:
            try:
                await self._playwright.stop()
            except Exception:
                pass
            self._playwright = None

    # -- 页面操作 --

    async def navigate(self, url: str) -> str:
        """导航到指定 URL"""
        try:
            await self.ensure_browser()
            assert self._page is not None
            await self._page.goto(url)
            return f"已访问 {url}"
        except Exception as exc:
            return f"导航失败: {exc}"

    async def get_content(self) -> str:
        """获取当前页面文本内容（最多 5000 字）"""
        try:
            await self.ensure_browser()
            assert self._page is not None
            content = await self._page.inner_text("body")
            return content[:5000]
        except Exception as exc:
            return f"读取内容失败: {exc}"

    async def click(self, selector: str) -> str:
        """点击匹配 CSS 选择器的元素"""
        try:
            await self.ensure_browser()
            assert self._page is not None
            await self._page.click(selector)
            return f"已点击元素: {selector}"
        except Exception as exc:
            return f"点击失败: {exc}"

    async def fill(self, selector: str, text: str) -> str:
        """在输入框中填入文本"""
        try:
            await self.ensure_browser()
            assert self._page is not None
            await self._page.fill(selector, text)
            return f"已在 {selector} 输入: {text}"
        except Exception as exc:
            return f"输入失败: {exc}"
