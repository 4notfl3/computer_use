"""shared — 跨 MCP server 的共享基础设施

核心组件:
    - config: 项目级配置常量（路径、模型名、清理参数等）
    - server_base: ServerConfig 数据类
    - registry: 服务注册与发现，launcher / host 通过它自动发现所有 server

用法:
    from shared.config import SCREENSHOT_DIR, BROWSER_CHANNEL
    from shared.registry import registry
    from shared.server_base import ServerConfig
"""

from shared.config import (
    BROWSER_CHANNEL,
    BROWSER_HEADLESS,
    SCREENSHOT_DIR,
    SCREENSHOT_TTL,
    WORKSPACE_DIR,
)
from shared.registry import registry
from shared.server_base import ServerConfig

__all__ = [
    "BROWSER_CHANNEL",
    "BROWSER_HEADLESS",
    "SCREENSHOT_DIR",
    "SCREENSHOT_TTL",
    "ServerConfig",
    "WORKSPACE_DIR",
    "registry",
]
