"""MCP 服务器统一启动器

用法:
    uv run python -m mcp_server.launcher all       # 一键启动所有工具
    uv run python -m mcp_server.launcher browser    # 单独启动浏览器
    uv run python -m mcp_server.launcher vision     # 单独启动截图分析
    uv run python -m mcp_server.launcher --list     # 列出所有可用服务器
"""

from __future__ import annotations

import importlib
import sys

from shared.registry import registry


def list_servers() -> None:
    """打印所有已注册的 MCP 服务器"""
    print("可用 MCP 服务器:")
    for cfg in registry.list_servers():
        tags = f" [{' / '.join(cfg.tags)}]" if cfg.tags else ""
        env = f" (需 {cfg.env_file})" if cfg.env_file else ""
        print(f"  {cfg.name}: {cfg.description}{tags}{env}")
    print()
    print("推荐: uv run python -m mcp_server.launcher all")


def launch(server_name: str) -> None:
    """按名称启动单个 MCP 服务器"""
    cfg = registry.get(server_name)
    if cfg is None:
        print(f"错误: 未知服务器 '{server_name}'")
        names = " / ".join(registry.list_names())
        print(f"可用: {names}")
        sys.exit(1)

    module_name, attr_name = cfg.module_path.split(":")
    module = importlib.import_module(module_name)
    mcp = getattr(module, attr_name)
    mcp.run(transport=cfg.transport)


def main(argv: list[str] | None = None) -> None:
    """入口：解析命令行参数并分发"""
    args = argv or sys.argv[1:]
    if not args:
        print("用法: uv run python -m mcp_server.launcher <服务器名>")
        print("提示: uv run python -m mcp_server.launcher --list")
        sys.exit(1)

    arg = args[0]
    if arg in ("--list", "-l"):
        list_servers()
    else:
        launch(arg)


if __name__ == "__main__":
    main()
