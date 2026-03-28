"""阿里云 Qwen-VL OCR 工具函数
使用 qwen-vl-ocr-latest 模型，识别效果业界顶尖
支持复杂文档、表格、公式、手写体识别
"""
import os
from pathlib import Path
from typing import Optional, Union


def extract_text_from_image(
    image_path: Union[str, Path],
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest',
    prompt: str = '请准确完整地识别图片中的所有文字内容'
) -> str:
    """从图片中提取文字
    
    Args:
        image_path: 图片文件路径
        api_key: 阿里云 API Key (可选，不传则从环境变量 DASHSCOPE_API_KEY 读取)
        model: OCR 模型名称，默认 qwen-vl-ocr-latest
        prompt: 提示词，可自定义识别要求
    
    Returns:
        识别出的文字内容
    
    Raises:
        ValueError: 未设置 API Key
        RuntimeError: 识别失败
    """
    import dashscope
    from dashscope import MultiModalConversation
    
    # 获取 API Key
    api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
    if not api_key:
        raise ValueError(
            "未找到阿里云 API Key\n"
            "请设置环境变量 DASHSCOPE_API_KEY 或在参数中传入\n"
            "获取地址：https://dashscope.console.aliyun.com/apiKey"
        )
    
    # 设置 API Key
    dashscope.api_key = api_key
    
    # 验证文件存在
    image_path = Path(image_path).expanduser()
    if not image_path.exists():
        raise FileNotFoundError(f"图片不存在：{image_path}")
    
    try:
        # 构建请求
        messages = [{
            'role': 'user',
            'content': [
                {'image': str(image_path.absolute())},
                {'text': prompt}
            ]
        }]
        
        # 调用 API
        response = MultiModalConversation.call(
            model=model,
            messages=messages
        )
        
        # 解析响应
        if response and hasattr(response, 'output'):
            output = response.output
            choices = output.get('choices', [])
            
            if choices and len(choices) > 0:
                message = choices[0].get('message', {})
                content = message.get('content', '')
                
                # content 可能是字符串或列表
                if isinstance(content, list):
                    text = '\n'.join([
                        item.get('text', '') if isinstance(item, dict) else str(item)
                        for item in content
                    ])
                elif isinstance(content, str):
                    text = content
                else:
                    text = str(content)
                
                return text.strip()
            else:
                raise RuntimeError("API 返回为空")
        else:
            raise RuntimeError(f"API 调用失败：{response}")
            
    except Exception as e:
        raise RuntimeError(f"OCR 识别失败：{e}")


def extract_text_with_details(
    image_path: Union[str, Path],
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest'
) -> dict:
    """从图片中提取文字，并返回详细信息
    
    Args:
        image_path: 图片文件路径
        api_key: 阿里云 API Key
        model: OCR 模型名称
    
    Returns:
        包含识别结果和调用详情的字典:
        - success: 是否成功
        - text: 识别的文字
        - request_id: 请求 ID
        - usage: 用量信息
        - error: 错误信息 (如果失败)
    """
    import dashscope
    from dashscope import MultiModalConversation
    
    try:
        # 获取 API Key
        api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        if not api_key:
            return {
                'success': False,
                'error': '未设置 API Key'
            }
        
        dashscope.api_key = api_key
        
        # 验证文件
        image_path = Path(image_path).expanduser()
        if not image_path.exists():
            return {
                'success': False,
                'error': f'图片不存在：{image_path}'
            }
        
        # 构建请求
        messages = [{
            'role': 'user',
            'content': [
                {'image': str(image_path.absolute())},
                {'text': '请准确完整地识别图片中的所有文字内容'}
            ]
        }]
        
        # 调用 API
        response = MultiModalConversation.call(
            model=model,
            messages=messages
        )
        
        # 解析响应
        if response and hasattr(response, 'output'):
            output = response.output
            choices = output.get('choices', [])
            
            if choices and len(choices) > 0:
                message = choices[0].get('message', {})
                content = message.get('content', '')
                
                # 处理 content
                if isinstance(content, list):
                    text = '\n'.join([
                        item.get('text', '') if isinstance(item, dict) else str(item)
                        for item in content
                    ])
                elif isinstance(content, str):
                    text = content
                else:
                    text = str(content)
                
                return {
                    'success': True,
                    'text': text.strip(),
                    'request_id': getattr(response, 'request_id', None),
                    'usage': getattr(response, 'usage', None)
                }
            else:
                return {
                    'success': False,
                    'error': 'API 返回为空'
                }
        else:
            return {
                'success': False,
                'error': f'API 调用失败：{response}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def batch_extract_texts(
    image_paths: list,
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest',
    verbose: bool = True
) -> list:
    """批量提取多个图片的文字
    
    Args:
        image_paths: 图片路径列表
        api_key: 阿里云 API Key
        model: OCR 模型名称
        verbose: 是否打印进度
    
    Returns:
        识别结果列表，每个元素包含:
        - path: 图片路径
        - text: 识别的文字 (如果成功)
        - error: 错误信息 (如果失败)
        - success: 是否成功
    """
    results = []
    
    for i, img_path in enumerate(image_paths, 1):
        if verbose:
            print(f"[{i}/{len(image_paths)}] 正在识别：{Path(img_path).name}...")
        
        result = extract_text_with_details(img_path, api_key, model)
        
        results.append({
            'path': str(img_path),
            'text': result.get('text', ''),
            'error': result.get('error', ''),
            'success': result.get('success', False)
        })
    
    return results


# 便捷函数
def ocr(image_path: str, **kwargs) -> str:
    """OCR 识别的便捷函数
    
    用法:
        text = ocr('image.jpg')
    
    Args:
        image_path: 图片路径
        **kwargs: 其他参数传递给 extract_text_from_image
    
    Returns:
        识别的文字
    """
    return extract_text_from_image(image_path, **kwargs)
