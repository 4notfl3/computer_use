"""VisionManager — 屏幕截图 + AI 图像分析

纯业务逻辑，零 MCP 框架依赖，可独立测试。
"""

from __future__ import annotations

import base64
import os
import threading
import time
from pathlib import Path
from openai import OpenAI
from PIL import ImageGrab

from shared.config import (
    DASHSCOPE_BASE_URL,
    DASHSCOPE_MODEL,
    SCREENSHOT_CLEANUP_INTERVAL,
    SCREENSHOT_DIR,
    SCREENSHOT_FORMATS,
    SCREENSHOT_TTL,
)


class VisionError(Exception):
    """视觉操作异常"""


class VisionManager:
    """管理屏幕截图与 AI 图像分析。

    截图默认保存到 workspace/screenshots/，支持自动清理过期文件。
    AI 分析通过阿里云 DashScope (OpenAI 兼容接口) 调用 Qwen 视觉模型。

    用法:
        manager = VisionManager()
        path = manager.take_screenshot()
        result = manager.analyze_image(path, "描述这张图片")
        manager.stop_cleanup()
    """

    def __init__(
        self,
        screenshot_dir: Path | str | None = None,
        api_key: str | None = None,
        base_url: str = DASHSCOPE_BASE_URL,
        model: str = DASHSCOPE_MODEL,
    ) -> None:
        self._screenshot_dir = Path(screenshot_dir or SCREENSHOT_DIR)
        self._screenshot_dir.mkdir(parents=True, exist_ok=True)

        self._api_key = api_key
        self._base_url = base_url
        self._model = model
        self._client: OpenAI | None = None

        self._cleanup_stop = threading.Event()
        self._cleanup_thread: threading.Thread | None = None
        self._start_cleanup()

    # -- 内部初始化 --

    def _get_client(self) -> OpenAI:
        """延迟初始化 OpenAI 客户端（首次调用 AI 分析时才加载 .env）"""
        if self._client is None:
            # 延迟导入 dotenv，只在真正需要 API 调用时才加载
            from dotenv import load_dotenv

            load_dotenv()
            key = self._api_key or os.getenv("DASHSCOPE_API_KEY")
            if not key:
                raise VisionError(
                    "缺少 DASHSCOPE_API_KEY，请在 .env 文件中配置或传入 api_key 参数"
                )
            self._client = OpenAI(api_key=key, base_url=self._base_url)
        return self._client

    # -- 截图 --

    def take_screenshot(self, filename: str = "") -> str:
        """对当前屏幕截图，返回保存路径"""
        try:
            if not filename:
                filename = f"screen_{int(time.time())}.png"
            file_path = self._screenshot_dir / filename
            img = ImageGrab.grab()
            img.save(str(file_path))
            return str(file_path)
        except Exception as exc:
            return f"截图失败: {exc}"

    # -- AI 分析 --

    def analyze_image(
        self,
        image_path: str,
        question: str,
        *,
        delete_after: bool = True,
    ) -> str:
        """使用 AI 视觉模型分析图片内容

        Args:
            image_path: 图片路径（绝对或相对于截图目录）
            question: 你想问关于这张图的什么问题
            delete_after: 分析后是否自动删除图片
        """
        try:
            path = Path(image_path)
            if not path.is_absolute():
                path = self._screenshot_dir / image_path
            if not path.exists():
                return f"错误：找不到图片 {path}"

            with open(path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")

            client = self._get_client()
            response = client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": question},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{encoded}"
                                },
                            },
                        ],
                    }
                ],
            )
            return response.choices[0].message.content or "(空响应)"
        except VisionError:
            raise
        except Exception as exc:
            return f"分析失败: {exc}"
        finally:
            if delete_after and path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass

    # -- 自动清理 --

    def _start_cleanup(self) -> None:
        """启动后台清理线程"""
        self._cleanup_thread = threading.Thread(
            target=self._cleanup_loop,
            daemon=True,
            name="vision-cleanup",
        )
        self._cleanup_thread.start()

    def _cleanup_loop(self) -> None:
        """清理循环：每 SCREENSHOT_CLEANUP_INTERVAL 秒扫描一次"""
        while not self._cleanup_stop.wait(SCREENSHOT_CLEANUP_INTERVAL):
            self._remove_expired()

    def _remove_expired(self) -> None:
        """删除超过 SCREENSHOT_TTL 秒的截图文件"""
        now = time.time()
        for f in self._screenshot_dir.iterdir():
            if f.is_file() and f.suffix.lower() in SCREENSHOT_FORMATS:
                try:
                    if now - f.stat().st_mtime > SCREENSHOT_TTL:
                        f.unlink()
                except OSError:
                    pass

    def stop_cleanup(self, timeout: float = 2.0) -> None:
        """停止后台清理线程"""
        if self._cleanup_thread is not None and self._cleanup_thread.is_alive():
            self._cleanup_stop.set()
            self._cleanup_thread.join(timeout)
