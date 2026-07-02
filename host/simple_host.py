"""Simple Host — 一键测试所有 MCP 服务

用法:
    uv run python -m host.simple_host
"""

from __future__ import annotations

import asyncio

from host.agent_host import AgentHost


async def demo() -> None:
    """演示：连接服务器 → 打开网页 → 读取内容"""
    async with AgentHost() as host:
        print("连接服务器...")
        for r in await host.connect_all():
            print(f"  {r}")

        host.print_tools()

        print("\n打开网页...")
        nav_result = await host.call_tool(
            "browser_navigate", {"url": "https://example.com"}
        )
        if nav_result.success and nav_result.content:
            print(f"  {nav_result.content[0]['text']}")
        else:
            print(f"  失败: {nav_result.error}")

        print("\n读取内容...")
        read_result = await host.call_tool("browser_read_content", {})
        if read_result.success and read_result.content:
            text = read_result.content[0]["text"]
            print(f"  {text[:200]}...")
        else:
            print(f"  失败: {read_result.error}")


if __name__ == "__main__":
    asyncio.run(demo())
