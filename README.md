# Computer Use

MCP 服务器项目，为智能体提供浏览器自动化、屏幕截图和图像分析等能力。

## 项目结构

```
mcp_server/
├── browser/          # 浏览器自动化
│   ├── main.py       # 入口
│   ├── engine.py     # 核心逻辑
│   └── tools.py      # MCP 工具
├── vision/           # 屏幕截图和图像分析
│   ├── main.py
│   ├── manager.py    # VisionManager
│   └── tools.py
└── shared/           # 共用代码
```

## 快速开始

```bash
uv sync
```

## 运行

```bash
# browser MCP
uv run mcp_server/browser/main.py

# vision MCP
uv run mcp_server/vision/main.py
```

## 工具

### Browser

| 工具 | 说明 | 参数 |
|------|------|------|
| `browser_navigate` | 打开网页 | `url` |
| `browser_click` | 点击元素 | `selector` (CSS) |
| `browser_fill` | 填写表单 | `selector`, `text` |
| `browser_read_content` | 读取页面内容 | - |

### Vision

| 工具 | 说明 | 参数 |
|------|------|------|
| `vision_screenshot` | 屏幕截图 | `filename` (可选) |
| `vision_analyze` | 分析图片 | `image_path`, `question` |

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

## 依赖

- FastMCP — MCP 服务器框架
- Playwright — 浏览器自动化
- Pillow — 截图
- OpenAI — AI 图像分析（阿里云 Qwen）

## 环境变量

`.env` 文件需要配置：
- `DASHSCOPE_API_KEY` — 阿里云 API 密钥（用于 vision 图片分析）
