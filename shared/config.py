"""项目级配置常量 — 所有硬编码值集中管理"""

from __future__ import annotations

from pathlib import Path

# ---- 工作区 ----
WORKSPACE_DIR = Path(__file__).resolve().parent.parent / "workspace"
SCREENSHOT_DIR = WORKSPACE_DIR / "screenshots"

# ---- 浏览器 ----
BROWSER_CHANNEL = "msedge"
BROWSER_HEADLESS = False
BROWSER_USER_DATA_DIRNAME = "browser_profile"

# ---- 截图 ----
SCREENSHOT_CLEANUP_INTERVAL = 300  # 秒
SCREENSHOT_TTL = 600  # 秒（保留 10 分钟）
SCREENSHOT_FORMATS = (".png", ".jpg", ".jpeg")

# ---- AI 视觉 ----
DASHSCOPE_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"
DASHSCOPE_MODEL = "qwen3.5-122b-a10b"
