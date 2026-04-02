from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import base64
from mcp.types import ImageContent, CallToolResult, TextContent
from pathlib import Path


@register("astrbot_plugin_read_local_image", "sunnyyang", "读取本地图片文件并使用 ImageContent 机制让 LLM 立即分析图片内容", "1.5.0")
class ReadLocalImagePlugin(Star):
    def __init__(self, context: Context, config: dict | None = None):
        super().__init__(context)
        # 读取配置，使用默认值作为 fallback（5MB）
        self.max_image_size = 5 * 1024 * 1024
        self.allowed_paths: list[Path] = []
        self.enable_path_restriction = True
        
        if config:
            # 配置单位为 MB，转换为字节
            max_size_mb = config.get("max_image_size_mb", 5)
            self.max_image_size = max_size_mb * 1024 * 1024
            
            allowed_paths_str = config.get("allowed_paths", [])
            # 将允许的路径转换为 Path 对象并解析为绝对路径
            self.allowed_paths = [Path(p).resolve() for p in allowed_paths_str if p]
            self.enable_path_restriction = config.get("enable_path_restriction", True)

    def _check_path_allowed(self, file_path: str) -> bool:
        """使用 pathlib.Path.is_relative_to 检查路径是否在允许的目录列表中。
        
        白名单为空时返回 True（与 enable_path_restriction 配合实现开关效果）。
        """
        file_path_obj = Path(file_path).resolve()
        
        # 如果允许路径列表为空，返回 True（配合 enable_path_restriction 作为开关）
        if not self.allowed_paths:
            return True
        
        for allowed_path in self.allowed_paths:
            if file_path_obj.is_relative_to(allowed_path):
                return True
        return False

    @filter.llm_tool(name="read_local_image")
    async def read_local_image(self, event: AstrMessageEvent, file_path: str):
        """
        读取本地图片文件并返回图片数据，让 LLM 能够立即分析图片内容。

        Args:
            file_path (string): 图片文件的路径

        Returns:
            图片数据
        """
        # 使用 Path.resolve() 获取绝对路径并解析符号链接
        file_path_obj = Path(file_path).resolve()
        abs_path = str(file_path_obj)

        # 检查文件是否存在
        if not file_path_obj.exists():
            return CallToolResult(content=[TextContent(type="text", text="Error: 文件不存在")])
        
        # 检查是否是文件
        if not file_path_obj.is_file():
            return CallToolResult(content=[TextContent(type="text", text="Error: 不是文件")])

        # 路径限制检查
        if self.enable_path_restriction and not self._check_path_allowed(file_path):
            return CallToolResult(content=[TextContent(type="text", text=f"Error: 路径限制，允许的路径：{[str(p) for p in self.allowed_paths]}")])

        # 检查文件格式
        ext = file_path_obj.suffix.lower()
        mime_map = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp'
        }
        if ext not in mime_map:
            return CallToolResult(content=[TextContent(type="text", text=f"Error: 不支持的格式 {ext}")])

        # 获取文件大小（使用 try-except 处理权限错误）
        try:
            file_size = file_path_obj.stat().st_size
        except PermissionError:
            return CallToolResult(content=[TextContent(type="text", text="Error: 读取文件大小需要权限")])
        
        if file_size > self.max_image_size:
            return CallToolResult(content=[TextContent(type="text", text=f"Error: 文件大小超过 {self.max_image_size // (1024*1024)}MB 限制 (当前：{file_size} bytes)")])

        # 读取图片数据（使用 try-except 处理各种 IO 错误）
        try:
            with open(file_path_obj, "rb") as f:
                image_data = f.read()
        except PermissionError:
            return CallToolResult(content=[TextContent(type="text", text="Error: 读取图片需要权限")])
        except IOError as e:
            return CallToolResult(content=[TextContent(type="text", text=f"Error: 读取图片失败：{e!s}")])
        
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
