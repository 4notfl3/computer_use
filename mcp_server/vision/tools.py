"""Vision MCP 工具注册 — 将 VisionManager 方法暴露为 MCP tools"""

from __future__ import annotations

from fastmcp import FastMCP

from mcp_server.vision.manager import VisionManager


def register_tools(mcp: FastMCP, vision: VisionManager) -> None:
    """将 vision 的截图和分析功能注册为 MCP 工具"""

    @mcp.tool()
    def vision_screenshot(filename: str = "") -> str:
        """对当前屏幕截图。

        若不提供文件名则自动生成（如 screen_1719000000.png）。
        返回保存的完整文件路径。
        """
        return vision.take_screenshot(filename)

    @mcp.tool()
    def vision_analyze(
        image_path: str, question: str, delete_after: bool = False
    ) -> str:
        """分析指定路径的图片内容。

        Args:
            image_path: 图片文件路径（绝对或相对于截图目录）
            question: 你想问关于这张图片的问题
            delete_after: 分析后是否自动删除图片（默认 False 保留）
        """
        return vision.analyze_image(image_path, question, delete_after=delete_after)
