# Computer Use

MCP 服务器项目：让 AI 智能体可以**操控浏览器**和**看懂屏幕截图**。

基于 [MCP 协议](https://modelcontextprotocol.io)，兼容 Claude Desktop、自定义 Agent 等。

---

## 功能

| 工具 | 说明 |
|------|------|
| `browser_navigate` | 打开网页 |
| `browser_click` | 点击页面元素 |
| `browser_fill` | 输入文本 |
| `browser_read_content` | 读取页面内容 |
| `vision_screenshot` | 截取屏幕 |
| `vision_analyze` | AI 分析图片内容 |

---

## 快速开始

```bash
# 1. 安装
uv sync

# 2. 配置（Vision 需要）
echo DASHSCOPE_API_KEY=你的key > .env

# 3. [推荐] 一键启动所有服务
uv run python -m mcp_server.launcher all
```

## 在代码中使用

```python
from host.agent_host import AgentHost

async with AgentHost() as host:
    await host.connect_all()
    await host.call_tool("browser_navigate", {"url": "https://example.com"})
    r = await host.call_tool("browser_read_content", {})
    print(r.content[0]["text"][:200])
```

---

## Claude Desktop 配置

```json
{
  "computer-use-mcp": {
    "command": "uv",
    "args": ["run", "python", "-m", "mcp_server.combined"],
    "transportType": "stdio"
  }
}
```

---

## 项目结构

```
computer_use/
├── mcp_server/     # 服务器
│   ├── combined.py # 一键启动所有工具
│   ├── browser/    # 浏览器自动化
│   └── vision/     # 截图 + AI 分析
├── host/           # Host 客户端
├── shared/         # 共享基础设施
└── workspace/      # 截图文件等
```

---

## 环境要求

- Windows（PIL 截图依赖）
- Python >= 3.10, uv
- Microsoft Edge（浏览器自动化）
- 阿里云 API Key（截图分析）

开发者详见 [AGENTS.md](./AGENTS.md)。
