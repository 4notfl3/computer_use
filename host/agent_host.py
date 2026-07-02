"""AgentHost — MCP Host 客户端

团队成员通过此类在自己的 agent 中连接和调用所有 MCP 服务。

用法:
    async with AgentHost() as host:
        await host.connect_all()
        result = await host.call_tool("browser_navigate", {"url": "https://example.com"})
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass, field
from typing import Any

from mcp import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client

from shared.registry import registry

logger = logging.getLogger("agent_host")


@dataclass
class ToolInfo:
    """工具元信息"""

    server_name: str
    name: str
    description: str
    input_schema: dict[str, Any] = field(default_factory=dict)


@dataclass
class ToolResult:
    """工具调用结果"""

    success: bool
    content: list[dict[str, Any]] = field(default_factory=list)
    error: str = ""


class AgentHost:
    """MCP Host — 管理多个 MCP Server 的连接和工具调用。

    自动发现 registry 中注册的所有 server，建立 stdio 连接，
    并缓存工具列表以便路由调用。
    """

    def __init__(self, server_names: list[str] | None = None) -> None:
        self._sessions: dict[str, ClientSession] = {}
        self._transports: dict[str, tuple[Any, Any]] = {}
        self._tools: dict[str, ToolInfo] = {}
        self._server_names = server_names or registry.list_names()

    # -- 上下文管理器 --

    async def __aenter__(self) -> "AgentHost":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.disconnect_all()

    # -- 连接管理 --

    async def connect_all(self) -> list[str]:
        """并发连接所有已注册的 MCP 服务器"""
        tasks = [self._connect_one(name) for name in self._server_names]
        return await asyncio.gather(*tasks)

    async def _connect_one(self, name: str) -> str:
        """连接单个 MCP 服务器"""
        if name in self._sessions:
            return f"[{name}] 已连接"

        cfg = registry.get(name)
        if cfg is None:
            return f"[{name}] 未找到配置"

        launch = registry.get_launch_args(name)
        if launch is None:
            return f"[{name}] 无法获取启动参数"

        try:
            params = StdioServerParameters(command=launch[0], args=launch[1])
            read, write = await stdio_client(params)  # type: ignore[misc]
            session = ClientSession(read, write)
            await session.initialize()
            self._sessions[name] = session
            self._transports[name] = (read, write)
            await self._cache_tools(name, session)
            count = len([t for t in self._tools.values() if t.server_name == name])
            return f"[{name}] 连接成功 ({count} 工具)"
        except Exception as exc:
            logger.exception("连接 %s 失败", name)
            return f"[{name}] 失败: {exc}"

    async def disconnect_all(self) -> None:
        """断开所有连接并清理资源"""
        for name in list(self._sessions):
            if name in self._transports:
                _, write = self._transports.pop(name)
                try:
                    await write.aclose()  # type: ignore[misc]
                except Exception:
                    pass
            self._sessions.pop(name, None)
        self._tools.clear()

    # -- 工具管理 --

    async def _cache_tools(self, server: str, session: ClientSession) -> None:
        """从 server 获取工具列表并缓存"""
        result = await session.list_tools()
        for t in result.tools:
            self._tools[t.name] = ToolInfo(
                server_name=server,
                name=t.name,
                description=t.description or "",
                input_schema=t.inputSchema,
            )

    def list_tools(self, server: str | None = None) -> list[ToolInfo]:
        """列出已发现的工具，可按 server 过滤"""
        if server:
            return [t for t in self._tools.values() if t.server_name == server]
        return list(self._tools.values())

    def print_tools(self) -> None:
        """打印所有可用工具"""
        print("\n可用工具:")
        for t in self._tools.values():
            print(f"  - {t.name}: {t.description}")

    # -- 工具调用 --

    async def call_tool(
        self, name: str, args: dict[str, Any] | None = None
    ) -> ToolResult:
        """调用指定工具并返回结果"""
        info = self._tools.get(name)
        if info is None:
            return ToolResult(success=False, error=f"未知工具: {name}")

        session = self._sessions.get(info.server_name)
        if session is None:
            return ToolResult(
                success=False,
                error=f"服务器 '{info.server_name}' 未连接",
            )

        try:
            result = await session.call_tool(name, args or {})
            content: list[dict[str, Any]] = []
            for c in result.content:
                item: dict[str, Any] = {"type": c.type}
                item["text"] = c.text if hasattr(c, "text") else str(c)
                content.append(item)
            return ToolResult(success=True, content=content)
        except Exception as exc:
            logger.exception("调用 %s 失败", name)
            return ToolResult(success=False, error=f"调用失败: {exc}")


# -- CLI 入口 --


async def main() -> None:
    """命令行交互入口"""
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    async with AgentHost() as host:
        print("连接 MCP 服务器...")
        for r in await host.connect_all():
            print(f"  {r}")
        host.print_tools()
        print("\n已连接。可调用 host.call_tool() 使用工具。")


if __name__ == "__main__":
    asyncio.run(main())
