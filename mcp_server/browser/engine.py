import os

from playwright.async_api import async_playwright


class BrowserManager:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        self.user_data_dir = os.path.join(os.getcwd(), "my_automation_profile")

    async def ensure_browser(self):
        """确保浏览器已启动，如果没有则启动"""
        if self.browser is None:
            self.playwright = await async_playwright().start()

        if self.context and self.context.is_closed():
            self.context = None
            self.page = None

        if self.context is None:
            self.browser = await self.playwright.chromium.launch(
                channel="msedge", headless=False
            )
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()

    async def navigate(self, url: str) -> str:
        """导航到指定页面"""
        try:
            await self.ensure_browser()
            await self.page.goto(url)
            return f"已访问 {url}"
        except Exception as e:
            return f"导航失败: {str(e)}"

    async def get_content(self) -> str:
        """获取页面内容，限制在前5000字以内"""
        try:
            await self.ensure_browser()
            content = await self.page.inner_text("body")
            return content[:5000]
        except Exception as e:
            return f"读取内容失败: {str(e)}"

    async def click(self, selector: str) -> str:
        """点击页面元素"""
        try:
            await self.ensure_browser()
            await self.page.click(selector)
            return f"已点击元素: {selector}"
        except Exception as e:
            return f"点击失败: {str(e)}"

    async def fill(self, selector: str, text: str) -> str:
        """在页面元素中输入文本"""
        try:
            await self.ensure_browser()
            await self.page.fill(selector, text)
            return f"已在 {selector} 输入: {text}"
        except Exception as e:
            return f"输入失败: {str(e)}"
