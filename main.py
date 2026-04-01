from astrbot.api.event import filter
from astrbot.api.star import Context, Star, register
from .tools.image_tool import read_image_as_base64

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件并返回 Base64 数据。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, file_path: str):
        """
        读取本地图片文件并返回 Base64 编码数据。
        
        Args:
            file_path (string): 图片文件的完整路径，例如 "/home/user/image.jpg"
        
        Returns:
            Base64 编码的图片数据，或错误信息
        """
        return await read_image_as_base64(file_path)