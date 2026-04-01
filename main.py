from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from .tools.image_tool import read_image_as_base64

@register("astrbot_plugin_read_local_image", "User", "读取本地图片文件并返回 Base64 数据。", "1.0.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件，让 LLM 能够看到并分析图片内容。
        
        Args:
            file_path (string): 图片文件的完整路径
        
        Returns:
            图片内容供 LLM 分析，或错误信息
        """
        result = await read_image_as_base64(file_path)
        
        if result.startswith("Error:"):
            return result
        
        try:
            # 解析 data URI: "data:image/jpeg;base64,xxxxx"
            header, b64_data = result.split(",", 1)
            mime_type = header.split(":")[1].split(";")[0]
            
            # 返回 Anthropic 格式的 image content block 列表
            # AstrBot 会把 llm_tool 的返回值作为 tool_result 内容传给 LLM
            # 返回 list 时，框架会将其作为多模态 content 处理
            return [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": mime_type,
                        "data": b64_data,
                    }
                },
                {
                    "type": "text",
                    "text": "图片已成功读取，请分析以上图片内容。"
                }
            ]
            
        except Exception as e:
            logger.error(f"[ReadLocalImage] 处理失败: {e}")
            return f"Error: 处理失败：{str(e)}"