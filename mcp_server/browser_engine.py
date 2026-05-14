import os
from playwright.async_api import async_playwright

# 浏览器管理类，负责启动浏览器、导航页面、获取内容等操作
class BrowserManager:
    def __init__(self, workspace):
        self.workspace = workspace
        self.context = None
        self.page = None
        self.playwright = None
        self.user_data_dir = os.path.join(os.getcwd(), "my_automation_profile")

    # 确保浏览器已启动，如果没有则启动
    async def ensure_browser(self):
        """确保浏览器已启动，如果没有则启动"""
        if self.browser is None:
            self.playwright = await async_playwright().start()

        # 如果浏览器已启动但上下文已关闭，重置浏览器实例
        if self.context and self.context.is_closed():
            self.context = None
            self.page = None

        # 如果浏览器未启动，启动浏览器并创建新页面
        if self.context is None:
            # headless=False 表示显示浏览器界面，方便调试
            self.browser = await self.playwright.chromium.launch(channel="msedge", headless=False)
            context = await self.browser.new_context()
            self.page = await context.new_page()

    # 导航到指定页面
    async def navigate(self, url: str):
        await self.ensure_browser()
        await self.page.goto(url)
        return f"已访问 {url}"

    # 获取页面内容，限制在前5000字以内，防止上下文过长
    async def get_content(self):
        await self.ensure_browser()
        # 获取页面可见文本
        content = await self.page.inner_text("body")
        return content[:5000] # 截取前5000字，防止上下文太长

    # 点击页面元素，selector是CSS选择器
    async def click(self, selector: str):
        await self.ensure_browser()
        await self.page.click(selector)
        return f"已点击元素: {selector}"

    # 在页面元素中输入文本，selector是CSS选择器，text是要输入的文本
    async def fill(self, selector: str, text: str):
        await self.ensure_browser()
        await self.page.fill(selector, text)
        return f"已在 {selector} 输入: {text}"