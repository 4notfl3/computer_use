def register_tools(mcp, browser_manager):

    @mcp.tool()
    async def browser_navigate(url: str) -> str:
        """打开或跳转到指定网址"""
        return await browser_manager.navigate(url)

    @mcp.tool()
    async def browser_click(selector: str) -> str:
        """点击页面上的元素 (支持 CSS 选择器，如 'button', '#submit', '.class')"""
        return await browser_manager.click(selector)

    @mcp.tool()
    async def browser_fill(selector: str, text: str) -> str:
        """在输入框输入内容"""
        return await browser_manager.fill(selector, text)

    @mcp.tool()
    async def browser_read_content() -> str:
        """读取当前页面的主要文本内容"""
        return await browser_manager.get_content()
