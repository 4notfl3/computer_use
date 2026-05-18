# mcp_server/vision/tools.py

from .manager import VisionManager

def register_tools(mcp, vision_manager: VisionManager):
    """
    注册 Vision 相关的工具到 MCP Server
    """

    @mcp.tool()
    def vision_screenshot(filename: str = "") -> str:
        """
        对当前屏幕进行截图。
        如果不提供文件名，将自动生成一个。
        返回保存的文件路径。
        """
        return vision_manager.take_screenshot(filename)

    @mcp.tool()
    def vision_analyze(image_path: str, question: str) -> str:
        """
        分析指定路径的图片内容。
        参数:
        - image_path: 截图保存的路径（例如 workspace/screenshots/xxx.png）
        - question: 你想问关于这张图的什么问题
        """
        # 这里我们构建了一个上下文：图片 + 用户的问题
        # 直接交给 Manager 去调用 AI
        return vision_manager.analyze_image(image_path, question)