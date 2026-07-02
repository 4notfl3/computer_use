"""vision — 截图 + AI 图像分析 MCP Server

支持全屏截图（Pillow ImageGrab）和 AI 视觉分析（阿里云 Qwen 模型）。
截图文件支持自动过期清理。
"""

from __future__ import annotations

from mcp_server.vision.manager import VisionManager

__all__ = ["VisionManager"]
