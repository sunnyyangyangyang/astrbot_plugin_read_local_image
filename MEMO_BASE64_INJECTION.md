# 备忘录：AstrBot Read Local Image 插件

## 1. 插件概述

本插件是一个纯粹的本地图片读取工具，让 LLM 可以通过 `read_local_image` 工具读取指定路径的图片文件。使用 AstrBot 的 `ImageContent` 机制，图片数据会立即注入到 LLM 上下文，LLM 在同一轮对话中即可分析图片内容。

## 2. 核心功能

### read_local_image 工具

**用途**：读取本地图片文件并通过 ImageContent 机制让 LLM 立即分析。

**参数**：
- `file_path` (string): 图片文件的完整路径

**返回**：
- 成功：`CallToolResult` 包含 `ImageContent`（AstrBot 自动注入到 LLM 上下文）
- 失败：错误信息（文件不存在、格式不支持等）

**支持格式**：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`

## 3. 设计原则

- **立即注入**：使用 AstrBot 内置的 `ImageContent` 机制
- **同一轮响应**：LLM 无需等待下一轮对话即可分析图片
- **纯本地**：只读取本地文件系统
- **错误友好**：返回清晰的错误信息

## 4. 实现说明

### main.py

- 使用 `@filter.llm_tool` 装饰器注册 LLM 工具
- 工具名称：`read_local_image`
- 读取图片文件并转换为 Base64
- 返回 `CallToolResult` 包含 `ImageContent`，AstrBot 自动处理注入

### ImageContent 机制

1. 工具读取本地图片文件
2. 转换为 Base64 编码
3. 返回 `CallToolResult` 包含 `ImageContent`
4. AstrBot 自动缓存并注入到 LLM 上下文
5. LLM 在同一轮对话中即可看到并分析图片

---

**版本记录：** v1.5.0
**维护者：** User