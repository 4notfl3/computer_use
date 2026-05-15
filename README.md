# Computer Use

MCP 服务器项目，为智能体提供浏览器自动化等能力。

## 项目结构

每个 MCP server 是独立进程，遵循三层结构：

```
mcp_server/
├── browser/          # 浏览器自动化 server
│   ├── server.py     # 入口：创建 FastMCP 实例，启动服务
│   ├── engine.py     # 核心：业务逻辑（不依赖 FastMCP）
│   ├── tools.py      # 接口：用 @mcp.tool() 包装 engine 方法
│   └── __init__.py
├── weather/          # 天气 server（待开发）
├── shared/           # 多 server 共用代码
```

新增 server 只需在 `mcp_server/` 下按同样结构添加子目录。

## 快速开始

```bash
uv sync
uv pip install -e .
```

## 运行

```bash
uv run mcp_server/browser/server.py
```

## 测试
```
npx @modelcontextprotocol/inspector uv run mcp_server/browser/server.py   
 
```

## Browser 工具

| 工具 | 说明 | 参数 |
|------|------|------|
| `browser_navigate` | 打开网页 | `url` |
| `browser_click` | 点击元素 | `selector` (CSS) |
| `browser_fill` | 填写表单 | `selector`, `text` |
| `browser_read_content` | 读取页面内容 | 无 |

## Host 配置示例

```json
{
  "my-browser-mcp": {
    "command": "uv",
    "args": ["run", "mcp_server/browser/server.py"],
    "transportType": "stdio"
  }
}
```

## 依赖

- [FastMCP](https://github.com/jlowin/fastmcp) — MCP 服务器框架
- [Playwright](https://playwright.dev/python/) — 浏览器自动化