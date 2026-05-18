# MCP 服务器

## 目录结构

```
mcp_server/
├── browser/          # 浏览器自动化
│   ├── main.py       # 入口
│   ├── engine.py     # BrowserManager 类
│   └── tools.py      # MCP 工具定义
└── vision/           # 屏幕截图和图像分析
    ├── main.py
    ├── manager.py    # VisionManager 类
    └── tools.py
```

## 快速启动

```bash
# browser MCP
uv run mcp_server/browser/main.py

# vision MCP
uv run mcp_server/vision/main.py
```

## Claude Desktop 配置

```json
{
  "browser-mcp": {
    "command": "uv",
    "args": ["run", "mcp_server/browser/main.py"],
    "transportType": "stdio"
  },
  "vision-mcp": {
    "command": "uv",
    "args": ["run", "mcp_server/vision/main.py"],
    "transportType": "stdio"
  }
}
```
