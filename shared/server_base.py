"""MCP 服务器基础模块 — ServerConfig 数据类"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ServerConfig:
    """单个 MCP 服务器的注册配置"""

    name: str
    module_path: str  # 格式: "package.module:attribute"
    description: str = ""
    transport: str = "stdio"
    env_file: str | None = None
    tags: list[str] = field(default_factory=list)
