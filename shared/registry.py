"""MCP 服务注册与发现

所有 MCP server 在此登记，launcher / host / 其他团队成员
通过统一接口发现和连接服务。

用法:
    from shared.registry import registry
    for cfg in registry.list_servers():
        print(cfg.name, cfg.module_path)
"""

from __future__ import annotations

from shared.server_base import ServerConfig

_SERVERS: dict[str, ServerConfig] = {
    "browser": ServerConfig(
        name="browser",
        module_path="mcp_server.browser.main:mcp",
        description="浏览器自动化 — Playwright 驱动本地 Edge",
        tags=["automation", "playwright"],
    ),
    "vision": ServerConfig(
        name="vision",
        module_path="mcp_server.vision.main:mcp",
        description="截图 + AI 图像分析 — 阿里云 Qwen 视觉模型",
        env_file=".env",
        tags=["vision", "screenshot", "ai"],
    ),
    "all": ServerConfig(
        name="all",
        module_path="mcp_server.combined:mcp",
        description="一键启动 — 包含所有工具（推荐）",
        tags=["all"],
    ),
}


class ServerRegistry:
    def __init__(self, servers: dict[str, ServerConfig] | None = None) -> None:
        self._servers: dict[str, ServerConfig] = servers or {}

    def list_servers(self) -> list[ServerConfig]:
        return list(self._servers.values())

    def get(self, name: str) -> ServerConfig | None:
        return self._servers.get(name)

    def list_names(self) -> list[str]:
        return list(self._servers.keys())

    def filter_by_tag(self, tag: str) -> list[ServerConfig]:
        return [cfg for cfg in self._servers.values() if tag in cfg.tags]

    def register(self, config: ServerConfig) -> None:
        if config.name in self._servers:
            raise KeyError(f"服务器 '{config.name}' 已存在")
        self._servers[config.name] = config

    def get_launch_args(self, name: str) -> tuple[str, list[str]] | None:
        cfg = self.get(name)
        if cfg is None:
            return None
        module_name, _ = cfg.module_path.split(":")
        return ("uv", ["run", "python", "-m", module_name])


registry = ServerRegistry(_SERVERS)
