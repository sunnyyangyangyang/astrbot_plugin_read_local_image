from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.api import logger
import os

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件让 LLM 分析。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self._pending_images: dict[str, str] = {}  # uid -> 文件路径

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件，让 LLM 能够看到并分析图片内容。

        Args:
            file_path (string): 图片文件的完整路径，例如 "screenshots/xxx.jpeg"

        Returns:
            操作结果
        """
        # 转换为绝对路径
        abs_path = os.path.abspath(file_path)

        if not os.path.exists(abs_path):
            return f"Error: 文件不存在：{abs_path}"
        if not os.path.isfile(abs_path):
            return f"Error: 不是文件：{abs_path}"

        ext = os.path.splitext(abs_path)[1].lower()
        supported = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tif', '.tiff', '.svg', '.heic'}
        if ext not in supported:
            return f"Error: 不支持的格式 {ext}，支持：{', '.join(supported)}"

        # 直接保存文件路径，让 AstrBot 处理
        self._pending_images[event.unified_msg_origin] = abs_path
        logger.info(f"[ReadLocalImage] 保存文件路径：{abs_path}")
        return "图片已读取"

    @filter.on_llm_request()
    async def inject_image_to_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """在 LLM 请求发出前，把暂存的图片路径注入到 req.image_urls"""
        uid = event.unified_msg_origin
        if uid not in self._pending_images:
            return

        path = self._pending_images.pop(uid)
        req.image_urls.append(path)
        logger.info(f"[ReadLocalImage] 注入文件路径：{path}")