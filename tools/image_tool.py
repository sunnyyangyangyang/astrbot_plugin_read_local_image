import base64
import os

# 文件扩展名到 MIME 类型的映射
EXT_TO_MIME = {
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.png': 'image/png',
    '.gif': 'image/gif',
    '.bmp': 'image/bmp',
    '.webp': 'image/webp',
    '.svg': 'image/svg+xml',
}

async def read_image_as_base64(file_path: str):
    """
    读取本地图片文件并返回 data URI 格式的图片数据。
    
    Args:
        file_path (str): 图片文件的完整路径
    
    Returns:
        str: data URI 格式的图片数据 (data:image/xxx;base64,xxx)，或错误信息
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: 文件不存在：{file_path}"
        
        if not os.path.isfile(file_path):
            return f"Error: 文件是一个目录：{file_path}"
        
        # 检查文件扩展名
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in EXT_TO_MIME:
            return f"Error: 图片格式不支持：{ext} (支持：{', '.join(EXT_TO_MIME.keys())})"
        
        with open(file_path, "rb") as f:
            image_data = f.read()
        
        b64_str = base64.b64encode(image_data).decode('utf-8')
        mime_type = EXT_TO_MIME[ext]
        
        # 返回 data URI 格式
        return f"data:{mime_type};base64,{b64_str}"
        
    except Exception as e:
        return f"Error: 读取图片失败：{str(e)}"
