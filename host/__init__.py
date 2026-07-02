"""host — MCP Host 客户端

提供连接 MCP 服务器、发现和调用工具的能力。

主要组件:
    - AgentHost: MCP Host，自动连接、发现、调用工具

用法:
    from host.agent_host import AgentHost

    async with AgentHost() as host:
        await host.connect_all()
        result = await host.call_tool("browser_navigate", {"url": "https://example.com"})
"""

from host.agent_host import AgentHost

__all__ = ["AgentHost"]
