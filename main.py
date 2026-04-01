from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.provider import ProviderRequest
from astrbot.api import logger
import os
import shutil

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件让 LLM 分析。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self._pending_images: dict[str, str] = {}  # uid -> 临时文件路径

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件，让 LLM 能够看到并分析图片内容。

        Args:
            file_path (string): 图片文件的完整路径，例如 "screenshots/xxx.jpeg"

        Returns:
            操作结果
        """
        abs_path = os.path.abspath(file_path)

        if not os.path.exists(abs_path):
            return f"Error: 文件不存在：{abs_path}"
        if not os.path.isfile(abs_path):
            return f"Error: 不是文件：{abs_path}"

        ext = os.path.splitext(abs_path)[1].lower()
        supported = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tif', '.tiff', '.svg', '.heic'}
        if ext not in supported:
            return f"Error: 不支持的格式 {ext}，支持：{', '.join(supported)}"

        # 将图片复制到临时目录，注入文件路径
        temp_dir = self._get_temp_dir()
        temp_file = os.path.join(temp_dir, f"img_{os.path.basename(abs_path)}")
        
        try:
            shutil.copy2(abs_path, temp_file)
            self._pending_images[event.unified_msg_origin] = temp_file
            logger.info(f"[ReadLocalImage] 图片已复制到临时目录：{temp_file}")
            return "图片已读取"
        except Exception as e:
            return f"Error: 复制图片失败：{e}"

    def _get_temp_dir(self):
        """获取临时目录，如果不存在则创建"""
        temp_dir = os.path.join(os.path.expanduser("~"), ".astrbot", "plugin_temp", "read_local_image")
        os.makedirs(temp_dir, exist_ok=True)
        return temp_dir

    @filter.on_llm_request()
    async def inject_image_to_request(self, event: AstrMessageEvent, req: ProviderRequest):
        """在 LLM 请求发出前，把暂存的图片路径注入到 req.image_urls"""
        uid = event.unified_msg_origin
        if uid not in self._pending_images:
            return

        path = self._pending_images.pop(uid)
        req.image_urls.append(path)
        logger.info(f"[ReadLocalImage] 注入文件路径：{path}")