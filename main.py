from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Image  # 或者 AstrBotMessage，看框架版本
from .tools.image_tool import read_image_as_base64
import base64
import os

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件并返回 Base64 数据。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件，让 LLM 能够看到并分析图片内容。
        
        Args:
            file_path (string): 图片文件的完整路径，例如 "/home/user/image.jpg" 或截图工具返回的路径
        
        Returns:
            图片内容供 LLM 分析，或错误信息
        """
        result = await read_image_as_base64(file_path)
        
        if result.startswith("Error:"):
            return result  # 错误信息直接返回文字就行
        
        # result 是 "data:image/jpeg;base64,xxxxx"
        # 需要把它注入到 LLM 的上下文里作为 image block
        try:
            # 解析 data URI
            header, b64_data = result.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]  # "image/jpeg"
            
            # 通过 event 把图片注入给 LLM（作为 tool result 的图片内容）
            # AstrBot 的做法：往 llm_context 里塞图片
            event.extra["image_results"] = event.extra.get("image_results", [])
            event.extra["image_results"].append({
                "type": "base64",
                "media_type": mime_type,
                "data": b64_data,
            })
            
            return f"图片已读取成功（{mime_type}），你现在可以直接分析图片内容了。"
            
        except Exception as e:
            logger.error(f"[ReadLocalImage] 注入图片失败: {e}")
            return f"Error: 图片读取成功但注入失败：{str(e)}"