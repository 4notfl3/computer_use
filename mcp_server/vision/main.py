# mcp_server/vision/main.py

from fastmcp import FastMCP

from mcp_server.vision.manager import VisionManager
from mcp_server.vision.tools import register_tools

# 创建 MCP 实例
mcp = FastMCP("Vision-Server")

# 实例化管理器 (保持状态，比如截图目录配置)
vision_manager = VisionManager()

# 注册工具
register_tools(mcp, vision_manager)

# 启动入口
if __name__ == "__main__":
    mcp.run(transport="stdio")
