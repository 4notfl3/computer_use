# mcp_server/vision/manager.py

import os
import base64
import time
from pathlib import Path
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
from PIL import ImageGrab  # 用于系统截图

# 加载环境变量
load_dotenv()

class VisionManager:
    def __init__(self):
        # 1. 初始化截图保存目录 (放在 workspace/screenshots 下)
        self.screenshot_dir = Path(__file__).parent.parent.parent / "workspace" / "screenshots"
        self.screenshot_dir.mkdir(parents=True, exist_ok=True)

        # 2. 初始化 AI 客户端 (qwen3.5-122b-a10b)
        self.client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

    def take_screenshot(self, filename: Optional[str] = None) -> str:
        """
        执行系统截图并保存到指定文件夹
        """
        try:
            if not filename:
                filename = f"screen_{int(time.time())}.png"
            
            file_path = self.screenshot_dir / filename
            
            # 使用 PIL ImageGrab 进行截图
            img = ImageGrab.grab()
            img.save(file_path)
            
            return f"截图成功，已保存至: {str(file_path)}"
        except Exception as e:
            return f"截图失败: {str(e)}"

    def analyze_image(self, image_path: str, prompt: str) -> str:
        """
        读取图片并调用 qwen 进行识别分析
        """
        try:
            # 确保路径是绝对路径
            path = Path(image_path)
            if not path.is_absolute():
                # 如果传进来的是相对路径，尝试在截图目录下寻找
                path = self.screenshot_dir / image_path

            if not path.exists():
                return f"错误：找不到图片文件 {path}"

            # 图片转 Base64
            with open(path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # 调用 qwen3.5-122b-a10b
            response = self.client.chat.completions.create(
                model="qwen3.5-122b-a10b", # 你的指定模型
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{encoded_image}"
                                },
                            },
                        ],
                    }
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"识别分析失败: {str(e)}"