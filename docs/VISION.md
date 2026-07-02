# Vision MCP Server

屏幕截图和 AI 图像分析。

## 工具

| 工具 | 说明 |
|------|------|
| `vision_screenshot` | 截图当前屏幕，返回保存路径 |
| `vision_analyze` | 分析指定图片内容 |

## 配置

需要创建 `.env` 文件：
```ini
DASHSCOPE_API_KEY=your_api_key_here
```

前往 [阿里云百炼平台](https://bailian.console.aliyun.com) 获取 API Key。

## 使用示例

```python
# 截图
result = await host.call_tool("vision_screenshot", {"filename": "my.png"})

# 分析图片
result = await host.call_tool("vision_analyze", {
    "image_path": "workspace/screenshots/my.png",
    "question": "描述这张图片",
    "delete_after": True,
})
```
