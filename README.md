# AstrBot Plugin: Read Local Image (v1.5.0)

一个简单的 AstrBot 插件，提供一个工具让 LLM 可以读取本地图片文件并立即分析。

## 功能

插件提供一个名为 `read_local_image` 的函数工具，LLM 可以调用它来读取指定路径的本地图片文件。插件会将图片数据注入到 LLM 上下文，让 LLM **在同一轮对话中**即可看到并分析图片内容。

## 工具说明

### read_local_image

**用途**：读取本地图片文件并让 LLM 立即分析图片内容。

**参数**：
- `file_path` (string): 图片文件的完整路径，例如 `/home/user/image.jpg`

**返回**：
- 成功时：返回图片数据（通过 AstrBot 的 `ImageContent` 机制自动注入）
- 失败时：返回错误信息（如文件不存在、格式不支持等）

**支持格式**：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`

## 安装与使用

1. 将插件放置在 `data/plugins/` 目录下。
2. 在 AstrBot WebUI 中重载插件。
3. LLM 会自动发现 `read_local_image` 工具，可以根据需要调用。

## 使用示例

用户："读取 `/home/sunny/picture.png` 这张图片并告诉我里面有什么"

LLM 会调用工具：
```
read_local_image(file_path="/home/sunny/picture.png")
```

插件会将图片数据注入到 LLM 上下文，LLM **在同一轮对话中**即可分析图片内容并回复：
> 图片中显示的是一个...（直接描述图片内容）

## 特点

- **立即注入**：使用 AstrBot 内置的 `ImageContent` 机制，图片数据自动注入到 LLM 上下文
- **同一轮响应**：LLM 无需等待下一轮对话，即可看到并分析图片
- **纯本地文件读取**：无需网络连接，支持本地文件路径
- **支持常见图片格式**：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`
- **简单的错误处理**：返回友好的错误信息

## 技术实现

插件使用 AstrBot 的 `ImageContent` 机制：
1. 工具读取本地图片文件
2. 转换为 Base64 编码
3. 返回 `CallToolResult` 包含 `ImageContent`
4. AstrBot 自动缓存并注入到 LLM 上下文
5. LLM 在同一轮对话中即可看到图片

## 版本历史

- **v1.5.0** (当前版本)
  - 使用 `ImageContent` 实现立即注入
  - LLM 在同一轮对话中即可分析图片
  - 支持格式：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`

- **v1.0.0**
  - 使用 `on_llm_request` hook 注入文件路径
  - 图片在下一轮 LLM 请求时注入（proof of concept）