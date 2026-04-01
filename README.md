# AstrBot Plugin: Read Local Image (v1.0.0)

一个简单的 AstrBot 插件，提供一个工具让 LLM 可以读取本地图片文件。

## 功能

插件提供一个名为 `read_local_image` 的函数工具，LLM 可以调用它来读取指定路径的本地图片文件，返回 Base64 编码的图片数据。

## 工具说明

### read_local_image

**用途**：读取本地图片文件并返回 Base64 编码数据。

**参数**：
- `file_path` (string): 图片文件的完整路径，例如 `/home/user/image.jpg`

**返回**：
- 成功时：返回图片的 Base64 编码数据
- 失败时：返回错误信息（如文件不存在、格式不支持等）

**支持格式**：`.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.webp`, `.svg`

## 安装与使用

1. 将插件放置在 `data/plugins/` 目录下。
2. 在 AstrBot WebUI 中重载插件。
3. LLM 会自动发现 `read_local_image` 工具，可以根据需要调用。

## 使用示例

用户："读取 `/home/sunny/picture.png` 这张图片"

LLM 会调用工具：
```
read_local_image(file_path="/home/sunny/picture.png")
```

插件返回图片的 Base64 数据，LLM 可以进一步处理或展示给用户。

## 特点

- 纯本地文件读取，无需网络连接
- 支持常见图片格式
- 简单的错误处理，返回友好的错误信息