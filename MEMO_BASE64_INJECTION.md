# 备忘录：AstrBot Read Local Image 插件

## 1. 插件概述

本插件简化为一个纯粹的本地图片读取工具，让 LLM 可以通过 `read_local_image` 工具读取指定路径的图片文件。

## 2. 核心功能

### read_local_image 工具

**用途**：读取本地图片文件并返回 Base64 编码数据。

**参数**：
- `file_path` (string): 图片文件的完整路径

**返回**：
- 成功：Base64 编码的图片数据
- 失败：错误信息（文件不存在、格式不支持等）

**支持格式**：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`

## 3. 设计原则

- **简单直接**：不需要网络下载、缓存检查、上下文提取
- **纯本地**：只读取本地文件系统
- **错误友好**：返回清晰的错误信息

## 4. 实现说明

### main.py
- 使用 `@filter.llm_tool` 装饰器注册 LLM 工具
- 工具名称：`read_local_image`
- 调用 `tools/image_tool.py` 中的 `read_image_as_base64` 函数

### tools/image_tool.py
- 验证文件存在
- 验证是文件（非目录）
- 验证扩展名合法
- 读取文件并转换为 Base64

---

**版本记录：** v1.0.0
**维护者：** User