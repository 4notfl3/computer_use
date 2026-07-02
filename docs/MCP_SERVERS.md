# MCP 服务器

项目通过 `shared/registry.py` 实现服务注册与发现。所有 MCP server 在此统一登记，
供 launcher、host、以及其他团队成员编写的 host 自动发现和连接。

## 注册表机制

```python
from shared.registry import registry

# 列出所有服务器
for cfg in registry.list_servers():
    print(cfg.name, cfg.module_path)

# 获取单个服务器
cfg = registry.get("browser")

# 按标签过滤
vision_servers = registry.filter_by_tag("vision")
```

## 当前服务器

| 名称 | 说明 | 标签 | 需要 .env |
|------|------|------|-----------|
| browser | 浏览器自动化 (Playwright + Edge) | automation, playwright, edge | 否 |
| vision | 截图 + AI 图像分析 (Qwen) | vision, screenshot, qwen, ai | 是 |

## 添加新服务器

1. 在 `mcp_server/` 下创建子包（engine + tools + main）
2. 在 `shared/registry.py` 的 `_SERVERS` 字典中添加一条配置
3. 启动: `uv run python -m mcp_server.launcher <name>`
4. Host 端自动发现: `await host.connect_all()`
