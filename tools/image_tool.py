import base64
import os

async def read_image_as_base64(file_path: str):
    """
    读取本地图片文件并返回 Base64 编码数据。
    
    Args:
        file_path (str): 图片文件的完整路径
    
    Returns:
        str: Base64 编码的图片数据，或错误信息
    """
    try:
        if not os.path.exists(file_path):
            return f"Error: 文件不存在：{file_path}"
        
        if not os.path.isfile(file_path):
            return f"Error: 文件是一个目录：{file_path}"
        
        # 检查文件扩展名
        valid_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in valid_extensions:
            return f"Error: 图片格式不支持：{ext} (支持：{', '.join(valid_extensions)})"
        
        with open(file_path, "rb") as f:
            image_data = f.read()
        
        b64_str = base64.b64encode(image_data).decode('utf-8')
        return b64_str
        
    except Exception as e:
        return f"Error: 读取图片失败：{str(e)}"