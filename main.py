from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.api import logger
import os
import base64
from mcp.types import ImageContent, CallToolResult, TextContent

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件让 LLM 分析。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件并返回图片数据，让 LLM 能够立即分析图片内容。

        Args:
            file_path (string): 图片文件的完整路径，例如 "screenshots/xxx.jpeg"

        Returns:
            图片数据
        """
        abs_path = os.path.abspath(file_path)

        if not os.path.exists(abs_path):
            return "Error: 文件不存在"
        if not os.path.isfile(abs_path):
            return "Error: 不是文件"

        ext = os.path.splitext(abs_path)[1].lower()
        mime_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp'
        }
        if ext not in mime_map:
            return f"Error: 不支持的格式 {ext}"

        with open(abs_path, "rb") as f:
            image_data = f.read()
        b64_str = base64.b64encode(image_data).decode('utf-8')
        mime_type = mime_map[ext]

        logger.info(f"[ReadLocalImage] 读取图片：{abs_path} ({len(image_data)} bytes)")

        # 返回 ImageContent，让 AstrBot 自动缓存并注入到 LLM 上下文
        return CallToolResult(
            content=[
                ImageContent(
                    type="image",
                    data=b64_str,
                    mimeType=mime_type
                )
            ]
        )