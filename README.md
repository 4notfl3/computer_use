# Computer Use

基于 MCP 的浏览器自动化服务器，让 AI 能够控制浏览器完成任务。

## 功能

- 🌐 **页面导航** - 打开任意网址
- 🖱️ **点击操作** - 通过 CSS 选择器点击页面元素
- ⌨️ **表单填充** - 在输入框中填写内容
- 📖 **内容读取** - 获取页面文本内容

## 安装

```bash
# 安装依赖
uv sync

# 安装浏览器
playwright install chromium
```

## 运行

```bash
python main.py
```

## 可用工具

| 工具名 | 说明 | 参数 |
|--------|------|------|
| `browser_navigate` | 打开网页 | `url`: 网址 |
| `browser_click` | 点击元素 | `selector`: CSS 选择器 |
| `browser_fill` | 填写表单 | `selector`, `text` |
| `browser_read_content` | 读取页面内容 | 无 |

## 示例

```python
# 导航到网页
browser_navigate(url="https://example.com")

# 点击按钮
browser_click(selector="#submit-button")

# 填写输入框
browser_fill(selector="#username", text="admin")

# 读取页面内容
browser_read_content()
```

## 依赖

- [FastMCP](https://github.com/jlowin/fastmcp) - MCP 服务器框架
- [Playwright](https://playwright.dev/python/) - 浏览器自动化