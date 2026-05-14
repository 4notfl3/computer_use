# AGENTS.md - Computer Use 项目

本文档为在此代码库工作的 AI 编程代理提供指导。

## 项目概述

这是一个 Python MCP (Model Context Protocol) 服务器，使用 FastMCP 和 Playwright 提供浏览器自动化能力。通过 MCP 接口暴露导航、点击、填充表单和读取页面内容等工具。

## 构建/检查/测试命令

### 环境配置
```bash
# 创建虚拟环境并安装依赖
uv sync

# 安装 Playwright 浏览器（首次运行必须）
playwright install chromium
```

### 运行服务器
```bash
# 运行 MCP 服务器
uv run python main.py
```

### 测试
```bash
# 运行所有测试
pytest

# 运行单个测试文件
pytest tests/test_browser.py

# 运行单个测试函数
pytest tests/test_browser.py::test_navigate

# 详细输出
pytest -v

# 带覆盖率报告
pytest --cov=mcp tests/
```

### 代码检查和类型检查
```bash
# 运行 ruff 代码检查
ruff check .

# 运行 ruff 格式检查
ruff format --check .

# 运行 ruff 格式化（自动修复）
ruff format .

# 运行 mypy 类型检查
mypy .
```

## 代码风格指南

### 导入
- 标准库导入在前，第三方库导入在中，本地模块导入在后
- 本地模块使用绝对导入：`from mcp.browser_engine import BrowserManager`
- 各组导入之间用空行分隔
- 每组内按字母顺序排序

示例：
```python
from pathlib import Path

from fastmcp import FastMCP
from playwright.async_api import async_playwright

from mcp.browser_engine import BrowserManager
from mcp.tools import register_tools
```

### 格式化
- 使用 4 个空格缩进（Python 标准）
- 最大行长度：88 字符（ruff 默认值）
- 字符串使用双引号
- 行尾无空格
- 文件末尾应有换行符

### 类型注解
- 使用 Python 3.10+ 类型注解语法（无需 `from typing import Optional`，使用 `X | None`）
- 为函数参数和返回值添加类型注解
- 异步函数使用 `async def`

示例：
```python
async def navigate(self, url: str) -> str:
    ...

def get_content(self) -> str | None:
    ...
```

### 命名规范
- **类名**：PascalCase（如 `BrowserManager`）
- **函数/方法名**：snake_case（如 `ensure_browser`、`get_content`）
- **常量**：UPPER_SNAKE_CASE（如 `WORKSPACE`）
- **私有方法**：以下划线开头（如 `_internal_helper`）
- **变量**：snake_case（如 `browser_manager`、`workspace`）

### 错误处理
- 对预期错误使用 try/except
- MCP 工具响应返回描述性错误消息字符串
- 适当记录错误日志
- 避免使用裸 `except:` 子句

示例：
```python
async def navigate(self, url: str) -> str:
    try:
        await self.ensure_browser()
        await self.page.goto(url)
        return f"已访问 {url}"
    except Exception as e:
        return f"导航失败: {str(e)}"
```

### 文档注释
- 代码注释使用中文（与现有代码库保持一致）
- 为公共函数和类添加文档字符串
- 使用三重双引号

示例：
```python
async def click(self, selector: str) -> str:
    """点击页面元素
    
    Args:
        selector: CSS选择器
        
    Returns:
        操作结果描述
    """
```

### 异步模式
- 所有 Playwright 操作使用 `async/await`
- 使用 ensure 方法延迟初始化资源
- 适当时使用 `async with` 上下文管理器

示例：
```python
async def ensure_browser(self):
    """确保浏览器已启动，如果没有则启动"""
    if self.browser is None:
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
```

### 项目结构
```
computer_use/
├── main.py              # 入口文件，MCP 服务器配置
├── mcp/
│   ├── browser_engine.py  # BrowserManager 类
│   └── tools.py           # MCP 工具定义
├── workspace/           # 浏览器下载/工作目录
├── pyproject.toml       # 项目配置
└── .python-version      # Python 版本 (3.10)
```

### 依赖
- `fastmcp` - MCP 服务器框架
- `playwright` - 浏览器自动化
- `playwright-stealth` - Playwright 隐身模式

### MCP 工具指南
- 每个工具应该是简单的异步函数，使用 `@mcp.tool()` 装饰器
- 返回用户友好的消息字符串
- 文档字符串和用户消息使用中文
- 工具应保持单一职责

### 提交前检查
1. 运行代码检查：`ruff check .`
2. 格式化代码：`ruff format .`
3. 运行类型检查：`mypy .`
4. 运行测试：`pytest`

## 注意事项
- 代码库使用中文注释和消息，请保持一致
- 这是 MCP 服务器项目，工具应尽可能保持无状态
- 浏览器实例由 BrowserManager 管理，采用延迟初始化


## Agent 的 MCP 配置文件
```python
"my-browser-mcp": {
  "disabled": false,
  "timeout": 60,
  "command": "uv",
  "args": ["run", "main.py"],
  "transportType": "stdio"
}
```
