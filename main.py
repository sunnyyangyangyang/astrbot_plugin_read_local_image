from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import os

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件让 LLM 分析。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        # 用于暂存待注入的图片路径，key = unified_msg_origin
        self._pending_images: dict[str, str] = {}

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件，让 LLM 能够看到并分析图片内容。

        Args:
            file_path (string): 图片文件的完整路径，例如 "screenshots/xxx.jpeg"
        
        Returns:
            操作结果提示
        """
        if not os.path.exists(file_path):
            return f"Error: 文件不存在：{file_path}"
        if not os.path.isfile(file_path):
            return f"Error: 不是文件：{file_path}"

        # 把路径暂存，等下一次 LLM 请求时注入
        uid = event.unified_msg_origin
        self._pending_images[uid] = os.path.abspath(file_path)
        logger.info(f"[ReadLocalImage] 暂存图片路径: {file_path}")
        return "图片已准备好，请直接描述你想对这张图片做什么分析。"

    @filter.on_decorating_result()
    async def inject_image(self, event: AstrMessageEvent):
        """在 LLM 请求发出前，把暂存的图片路径注入进去"""
        uid = event.unified_msg_origin
        if uid not in self._pending_images:
            return
        
        path = self._pending_images.pop(uid)
        if not os.path.exists(path):
            logger.warning(f"[ReadLocalImage] 注入时文件已不存在: {path}")
            return
        
        try:
            # AstrBot 官方方式：直接把本地路径传给 image_urls
            event.image_urls = getattr(event, 'image_urls', [])
            event.image_urls.append(path)
            logger.info(f"[ReadLocalImage] 注入成功: {path}")
        except Exception as e:
            logger.error(f"[ReadLocalImage] 注入失败: {e}")