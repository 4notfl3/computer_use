# 从本项目吃透 MCP

本文档从零开始讲解 MCP 协议的核心概念，结合本项目代码分析技术选型，
并讨论各种方案的优劣与改进方向。适合想通过实际项目学习 MCP 的开发者。

---

## 目录

1. [MCP 是什么](#1-mcp-是什么)
2. [MCP 核心概念](#2-mcp-核心概念)
3. [本项目架构拆解](#3-本项目架构拆解)
4. [技术栈深度分析](#4-技术栈深度分析)
5. [方案对比与改进方向](#5-方案对比与改进方向)
6. [常见问题](#6-常见问题)

---

## 1. MCP 是什么

MCP（Model Context Protocol）是 Anthropic 提出的**开放协议**，
类似于 AI 应用的 "USB-C 接口"——它定义了 AI 模型如何与外部工具/数据源交互的标准方式。

### 为什么需要 MCP？

在没有 MCP 之前，让 AI 调用工具通常是这样：

```
你写一个 API → AI 厂商提供 Function Calling → 你适配每家厂商的格式
```

问题：

- 每家 AI 的 Function Calling 格式不同（OpenAI / Claude / 本地模型）
- 工具和 AI 强耦合，换 AI 就要改代码
- 没有标准化的连接管理、安全、发现机制

MCP 解决了这些问题：

```
你写一个 MCP Server → 任何 MCP Host（Claude Desktop / 自定义 Agent）都能调用
```

### MCP vs 传统 API

| 对比维度 | 传统 REST API | MCP |
|---------|-------------|-----|
| 调用方式 | HTTP 请求 | 协议化的 Tool/Resource 调用 |
| 发现机制 | 需要文档 | `list_tools()` 自动发现 |
| 安全 | 自己实现认证 | 传输层管理 |
| 适用场景 | 前后端通信 | AI ↔ 工具的标准化交互 |
| 客户端 | 浏览器/代码 | AI Host（自动推理何时调用） |

---

## 2. MCP 核心概念

### 2.1 通信模型

```
┌─────────────┐         ┌──────────────┐
│  MCP Host    │         │  MCP Server  │
│  (Claude,    │ ◄─────► │  (这个项目)   │
│   你的 Agent)│  stdio  │              │
└─────────────┘         └──────────────┘
```

Host 和 Server 通过 **传输层（Transport）** 通信：

| 传输方式 | 说明 | 适用场景 |
|---------|------|---------|
| **stdio** | 子进程的标准输入输出 | 本地运行（本项目使用） |
| **SSE** | Server-Sent Events over HTTP | 远程服务器 |

### 2.2 核心原语

MCP 定义了三种能力：

```
Tools（工具）  ── 让 AI 可以执行动作（函数调用）
Resources（资源）── 让 AI 可以读取数据（类似文件系统）
Prompts（提示）── 让 AI 可以使用预设模板
```

本项目目前只用了 **Tools**，这是最常用且最容易理解的原语。

### 2.3 Tool 的生命周期

```
  Host                           Server
   │                               │
   ├── initialize() ──────────────► │  握手建立连接
   │                               │
   ├── list_tools() ──────────────► │  发现可用工具
   │◄──── tools 列表 ──────────────┤
   │                               │
   ├── call_tool("navigate",{url})►│  调用工具
   │◄──── 执行结果 ────────────────┤
   │                               │
   ├── call_tool("click",{selector})│  再次调用
   │◄──── 执行结果 ────────────────┤
```

**关键点：** 同一个 session 内，Server 保持状态（比如浏览器页面不会关闭）。
这意味着你可以先 navigate，再 click，再 read_content——浏览器一直是同一个。

### 2.4 FastMCP 做了什么

`fastmcp` 是一个简化 MCP Server 编写的框架。对比原生 MCP SDK：

**原生方式：**
```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [Tool(name="hello", inputSchema={"type": "object"})]

@server.call_tool()
async def call_tool(name, args):
    return [TextContent(type="text", text="Hello")]
```

**FastMCP 方式（本项目使用）：**
```python
from fastmcp import FastMCP
mcp = FastMCP("my-server")

@mcp.tool()
def hello() -> str:
    """说你好"""
    return "Hello"
```

FastMCP 自动处理：
- 函数签名 → JSON Schema 转换（参数类型自动推断）
- 文档字符串 → Tool 描述
- 返回值 → MCP Content 格式包装
- 生命周期管理

---

## 3. 本项目架构拆解

### 3.1 整体架构

```
┌─────────────────────────────────────────────────┐
│                   MCP Host                       │
│  (host/agent_host.py)                            │
│  自动连接 → 发现工具 → 路由调用                   │
└────────────────────┬────────────────────────────┘
                     │ stdio 通信
    ┌────────────────┼────────────────┐
    ▼                ▼                ▼
┌──────────┐  ┌──────────┐  ┌──────────────┐
│ browser  │  │  vision  │  │ combined(推荐)│
│ Server   │  │  Server  │  │ 所有工具合一   │
└──────────┘  └──────────┘  └──────────────┘
```

### 3.2 三层架构（每个 Server 内部）

```
mcp_server/browser/
├── main.py      层1: FastMCP 实例 + 启动入口
├── tools.py     层2: @mcp.tool() 注册
└── engine.py    层3: 纯业务逻辑
```

**为什么这样分层？**

| 层 | 职责 | 不做什么 |
|---|------|---------|
| main | 组装对象、启动进程 | 不写业务逻辑 |
| tools | 参数传递、注册到 MCP | 不写实现细节 |
| engine | 真正的业务实现 | 不导入 FastMCP |

**好处：**
- engine 可以独立测试（纯 Python，无框架依赖）
- 切换 MCP 框架时只改 tools 层
- 多人协作时职责清晰

### 3.3 注册表模式（shared/registry.py）

```python
_SERVERS = {
    "browser": ServerConfig(
        name="browser",
        module_path="mcp_server.browser.main:mcp",
        description="浏览器自动化",
        tags=["automation"],
    ),
}
```

**解决了什么问题？**

如果没有注册表，团队成员要加新 Server 需要：

1. 修改 launcher.py
2. 修改 host 连接代码
3. 告诉其他人手动连接

有了注册表：

- Launcher 自动发现：`mcp_server.launcher xxx`
- Host 自动连接：`AgentHost().connect_all()`
- 只需要**改一个地方**（registry.py）就全局生效

### 3.4 三种启动方式对比

```bash
# 方式一：分别启动（开发调试）
uv run python -m mcp_server.browser.main
uv run python -m mcp_server.vision.main

# 方式二：launcher 启动
uv run python -m mcp_server.launcher all

# 方式三：combined 服务器（推荐）
uv run python -m mcp_server.combined
```

**方式一**：各自独立进程，资源隔离，但管理麻烦
**方式二**：统一入口，但仍是一个进程
**方式三**：**推荐**，一个进程包含所有工具，通信开销最小

---

## 4. 技术栈深度分析

### 4.1 FastMCP vs 原生 MCP SDK

| 对比 | FastMCP | 原生 MCP SDK |
|-----|---------|-------------|
| 代码量 | 少（自动推断类型） | 多（手写 Schema） |
| 易用性 | 高（装饰器风格） | 低（需理解协议细节） |
| 灵活性 | 受框架限制 | 完全控制 |
| 社区 | 较新 | 官方维护 |
| 适用 | 快速开发工具 | 需要精细控制 |

**结论：** 本项目选 FastMCP 是正确的，工具类场景不需要精细控制。

### 4.2 Playwright（浏览器自动化）

Playwright 是一个浏览器自动化框架，与 Selenium 的对比：

| 对比 | Playwright | Selenium |
|-----|-----------|---------|
| 安装 | 自动下载浏览器 | 需手动装驱动 |
| API | 现代化 async/await | 回调式 |
| 速度 | 快 | 中等 |
| Edge 支持 | 原生支持 | 需要 WebDriver |
| 隐身模式 | playwright-stealth | 需额外配置 |

**本项目选 Playwright + Edge 的原因：**
- 日本地有 Edge，无需额外下载浏览器
- `playwright-stealth` 防止被网站检测为自动化

### 4.3 OpenAI 兼容接口（AI 图像分析）

本项目用 OpenAI Python SDK 调用阿里云 Qwen 视觉模型：

```python
from openai import OpenAI

client = OpenAI(
    api_key="your_dashscope_key",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)
```

**为什么不用阿里云官方 SDK？**
- OpenAI SDK 是业界标准接口
- 切换模型只需改 `base_url` 和 `api_key`
- 可以用同样的代码调用：OpenAI / 阿里云 / 本地 ollama

**支持的模型：**
- 阿里云 Qwen-VL（当前使用）
- 只需改 `model` 参数即可切换其他视觉模型

### 4.4 Pillow ImageGrab（截图）

```python
from PIL import ImageGrab
img = ImageGrab.grab()  # 全屏截图
```

**注意：** `ImageGrab` 在 Linux 上功能有限（需要 X server），
这也是为什么项目要求 Windows。

**替代方案：**
- Windows: `pyautogui.screenshot()` 功能类似
- 跨平台: `mss` (MSS) 库，速度更快
- 远程: VNC/RDP 截图

---

## 5. 方案对比与改进方向

### 5.1 当前架构的优缺点

**优点：**

1. **模块化好**：每个 Server 独立，可以单独开发测试
2. **扩展简单**：加新 Server 只需 4 步（创建目录 + registry 登记 + combined 引入）
3. **Host 友好**：其他团队成员只需 `AgentHost().connect_all()` 就能用所有工具
4. **关注点分离**：三层架构让业务逻辑和 MCP 框架解耦

**缺点/可改进点：**

| 问题 | 当前状态 | 改进方向 |
|------|---------|---------|
| 日志 | 无统一日志 | 加 structured logging |
| 错误处理 | 简单 try/except 返回字符串 | 定义错误码，结构化错误 |
| 多 Server 管理 | 单独进程或 unified | 可以 Docker 化 |
| 测试 | 几乎无测试 | 加 pytest + mock |
| 配置管理 | 硬编码 + .env | 加 YAML 配置文件 |
| 并发安全 | 未考虑 | BrowserManager 加锁 |

### 5.2 几种架构方案对比

```
方案 A（当前）：多个独立 Server 进程
  优点：资源隔离，一个崩溃不影响其他
  缺点：管理复杂，通信开销大
  适用：大型项目，不同团队维护不同 Server

方案 B（combined.py）：一个 Server 包含所有工具
  优点：启动简单，零通信开销
  缺点：一个模块崩溃影响全部
  适用：中小型项目，个人或小团队

方案 C：混合模式
  独立 Server + combined 并存
  开发时用 combined 快速调试
  生产部署用独立 Server 隔离
  本项目当前实际采用此方案 ✓
```

### 5.3 传输层选择

```
stdio（当前）：┌──── Host ────┐   stdin/stdout  ┌── Server ──┐
              │  子进程管理    │◄──────────────►│            │
              └──────────────┘                  └────────────┘

SSE（可选）：  ┌──── Host ────┐   HTTP/SSE     ┌── Server ──┐
              │  远程调用     │◄──────────────►│   HTTP     │
              └──────────────┘                  └────────────┘

WebSocket：    ┌──── Host ────┐   WebSocket    ┌── Server ──┐
              │  双向推送     │◄──────────────►│  持久连接   │
              └──────────────┘                  └────────────┘
```

| 方案 | 延迟 | 部署复杂度 | 适用场景 |
|-----|------|-----------|---------|
| stdio | 最低 | 最简单 | 本地运行（当前✅） |
| SSE | 中等 | 需要 HTTP 服务器 | 远程服务🎯 |
| WebSocket | 低 | 较复杂 | 实时通信需求 |

### 5.4 更好的目录结构（长远方向）

```
# 当前
computer_use/
├── mcp_server/       # 所有 Server 在一起
├── host/             # Host 客户端
└── shared/           # 共享代码

# 长远可选：Monorepo 风格
computer_use/
├── servers/
│   ├── browser/      # 独立包，有自己的 pyproject.toml
│   └── vision/       # 独立包
├── host/             # 不变
└── shared/           # 不变
```

独立包的好处：每个 Server 可以有自己的依赖和版本号，
但当前简单的架构不需要这么重。

### 5.5 如果重来，可以用什么替代

| 当前选型 | 替代方案 | 适合场景 |
|---------|---------|---------|
| FastMCP | 原生 MCP SDK, LangChain MCP | 需要精细控制时 |
| Playwright | Selenium, Puppeteer | 需要其他浏览器支持 |
| Pillow | mss (更快截图) | 截图性能敏感时 |
| OpenAI SDK | 阿里云官方 SDK | 只用阿里云时 |
| subprocess 管理 | Docker Compose | 需要容器化部署 |

---

## 6. 常见问题

### Q: 为什么启动后没有反应？

A: MCP Server 设计为 stdio 模式，启动后不会输出到终端。
它会等待 Host 发送协议消息。用 `uv run python -m host.simple_host` 来测试。

### Q: 多个 AI 同时调用会冲突吗？

A: 会的！当前 `BrowserManager` 没有加锁。
如果多个请求同时调用，浏览器状态会混乱。
改进方向：加 asyncio.Lock 或为每个 session 创建独立浏览器。

### Q: combined 和单独启动哪个好？

A: 开发测试用 combined 方便，线上部署用单独启动更稳定。
本项目两种都支持。

### Q: MCP 和 Function Calling 什么关系？

A: Function Calling 是各家 AI 自己定义的函数调用格式。
MCP 是标准化的协议层——它把各种 Function Calling 统一起来。
你的 MCP Server 写一次，OpenAI / Claude / 本地模型都能用。

### Q: 非 Python 项目能用 MCP 吗？

A: 可以。MCP 是协议，有 TypeScript/Java/Kotlin 等语言的 SDK。
只要实现 JSON-RPC 2.0 的 stdio/SSE 通信即可。

---

## 总结

```
MCP 的本质：让 AI 能调用工具的标准化协议
本项目的价值：用实际代码展示了如何构建 MCP Server
学习的关键：理解 Tool 生命周期 + 三层分层 + 注册表模式
改进的方向：错误处理、并发安全、日志、测试
```

这个项目虽然简单，但覆盖了 MCP 的核心场景。
掌握了这些，你就可以：

1. 为任何应用写 MCP Server
2. 理解 Claude Desktop 等工具的原理
3. 自己构建 AI Agent 系统
