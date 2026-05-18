# Vision MCP

屏幕截图和图像分析工具。

## 工具

### vision_screenshot
截图当前屏幕，返回保存路径。

### vision_analyze
分析指定图片内容。
- `image_path`: 图片路径
- `question`: 要问的问题

## 使用示例

```
vision_screenshot(filename="my.png")
vision_analyze("workspace/screenshots/my.png", "描述这张图片")
```

## 依赖

- `.env` 文件需要配置 `DASHSCOPE_API_KEY`
- 使用阿里云 Qwen3.5-122b-A10B 模型
