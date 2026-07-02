# AGENTS.md — 开发者指南

## 项目结构

```
computer_use/
├── mcp_server/            # MCP 服务器
│   ├── __init__.py
│   ├── combined.py        # [推荐] 一键启动所有工具
│   ├── launcher.py        # 统一启动器
│   ├── browser/           # 浏览器自动化 (Playwright + Edge)
│   │   ├── __init__.py
│   │   ├── main.py        # FastMCP 入口
│   │   ├── engine.py      # BrowserManager (纯业务, 零 FastMCP)
│   │   └── tools.py       # @mcp.tool() 注册
│   └── vision/            # 截图 + AI 分析 (Pillow + Qwen)
│       ├── __init__.py
│       ├── main.py        # FastMCP 入口
│       ├── manager.py     # VisionManager (含自动清理)
│       └── tools.py       # @mcp.tool() 注册
├── host/                  # MCP Host 客户端
│   ├── __init__.py
│   ├── agent_host.py      # AgentHost — 自动连接、路由调用
│   └── simple_host.py     # 测试示例
├── shared/                # 共享基础设施
│   ├── __init__.py
│   ├── config.py          # 项目级配置常量
│   ├── registry.py        # 服务注册表 (加新 server 需在此登记)
│   └── server_base.py     # ServerConfig 数据类
├── tests/                 # 测试套件
├── docs/                  # 详细文档
├── AGENTS.md              # 本文
└── README.md              # 用户说明
```

## 三层架构规范

| 层 | 文件 | 职责 | 依赖 |
|---|------|------|------|
| main | `main.py` | FastMCP 实例 + 启动 | tools |
| tools | `tools.py` | `@mcp.tool()` 定义工具 | engine/manager |
| engine | `engine.py` | 核心业务逻辑 | 零 FastMCP |

## 添加新 Server

1. 创建 `mcp_server/xxx/` 目录，包含 `main.py`, `engine.py`, `tools.py`
2. 在 `shared/registry.py` 的 `_SERVERS` 添加一条配置
3. 在 `mcp_server/combined.py` 引入并注册

```python
# shared/registry.py 添加:
"weather": ServerConfig(
    name="weather",
    module_path="mcp_server.weather.main:mcp",
    description="天气预报",
    tags=["weather"],
)

# mcp_server/combined.py 添加:
from mcp_server.weather.engine import WeatherManager
from mcp_server.weather.tools import register_tools as register_weather
weather = WeatherManager()
register_weather(mcp, weather)
```

完成后 launcher 和 host 自动发现，无需修改其他代码。

## 团队成员编写 Host

```python
from host.agent_host import AgentHost

async with AgentHost() as host:
    await host.connect_all()
    host.print_tools()  # 列出所有工具
    # 自动路由到正确服务器
    r = await host.call_tool("browser_navigate", {"url": "https://example.com"})
```

## 命令速查

```bash
uv sync                          # 安装依赖
uv run python -m mcp_server.launcher all       # [推荐] 一键启动
uv run python -m mcp_server.launcher browser   # 单独启动
uv run python -m mcp_server.launcher --list    # 列出服务器
uv run python -m host.simple_host              # 测试连接
uv run python -m host.agent_host               # 交互模式
ruff check . && ruff format .   # 代码检查
mypy .                          # 类型检查
```

## 代码风格

- 4 空格缩进，88 字符行宽，双引号字符串
- Python 3.10+ 类型: `X | None`, `list[X]`
- 导入顺序: 标准库 → 第三方 → 本地，每组按字母序
- 中文文档注释，公共函数/方法加文档字符串
- Engine/Manager 类支持 context manager 协议（`async with` 或 `with`）

## 配置管理

所有硬编码常量集中在 `shared/config.py`：

- `WORKSPACE_DIR`, `SCREENSHOT_DIR` — 工作区和截图路径
- `BROWSER_CHANNEL`, `BROWSER_HEADLESS` — 浏览器配置
- `SCREENSHOT_CLEANUP_INTERVAL`, `SCREENSHOT_TTL` — 截图清理策略
- `DASHSCOPE_BASE_URL`, `DASHSCOPE_MODEL` — AI 视觉模型配置

## 注意事项

- 截图目录 `workspace/screenshots/` 自动清理（默认保留 10 分钟）
- Vision server 需要 `.env` 中配置 `DASHSCOPE_API_KEY`
- `VisionManager` 采用延迟初始化，仅在首次调用 AI 分析时加载 `.env`
- 新增 server 需同时注册到 `registry.py` 和引入到 `combined.py`
- 浏览器延迟初始化，首次调用工具时自动启动；支持 `async with` 释放资源
