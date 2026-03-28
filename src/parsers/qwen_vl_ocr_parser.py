"""阿里云 Qwen-VL OCR 解析器
使用 qwen-vl-ocr-latest 模型，识别效果业界顶尖
支持复杂文档、表格、公式、手写体识别
"""
from pathlib import Path
from typing import List, Optional, Union
import os
from .base import BaseParser, Document


class QwenVLOCRParser(BaseParser):
    """阿里云 Qwen-VL OCR 解析器 - 云端识别，效果最优"""
    
    def __init__(
        self,
        file_path: Union[str, Path],
        api_key: Optional[str] = None,
        model: str = 'qwen-vl-ocr-latest',
        language: str = 'zh'
    ):
        """
        Args:
            file_path: 图片文件路径
            api_key: 阿里云 API Key (可选，不传则从环境变量 DASHSCOPE_API_KEY 读取)
            model: OCR 模型名称，默认 qwen-vl-ocr-latest
            language: 识别语言，'zh'=中文，'en'=英文，'auto'=自动检测
        """
        super().__init__(file_path)
        
        # 获取 API Key
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')
        if not self.api_key:
            raise ValueError(
                "未找到阿里云 API Key\n"
                "请设置环境变量 DASHSCOPE_API_KEY 或在构造函数中传入\n"
                "获取地址：https://dashscope.console.aliyun.com/apiKey"
            )
        
        self.model = model
        self.language = language
        self._client = None
    
    def _init_client(self):
        """初始化 DashScope 客户端"""
        if self._client is None:
            import dashscope
            from dashscope import MultiModalConversation
            
            # 设置 API Key
            dashscope.api_key = self.api_key
            
            self._client = MultiModalConversation()
    
    def parse(self) -> List[Document]:
        """执行 OCR 识别
        
        Returns:
            Document 列表，每个 Document 包含识别的文字和置信度
        """
        self.validate_file()
        self._init_client()
        
        try:
            # 使用 Qwen-VL 进行 OCR 识别
            from dashscope import MultiModalConversation
            
            # 构建请求
            messages = [
                {
                    'role': 'user',
                    'content': [
                        {'image': str(self.file_path.absolute())},
                        {'text': '请识别图片中的所有文字内容'}
                    ]
                }
            ]
            
            # 调用 API
            response = self._client.call(
                model=self.model,
                messages=messages
            )
            
            # 解析响应
            documents = []
            if response and hasattr(response, 'output') and response.output:
                # Qwen-VL 返回格式
                choices = response.output.get('choices', [])
                if choices and len(choices) > 0:
                    message = choices[0].get('message', {})
                    output_content = message.get('content', '')
                    
                    # output_content 可能是字符串或列表
                    if isinstance(output_content, list):
                        # 如果是列表，提取文本内容
                        output_text = '\n'.join([
                            item.get('text', '') if isinstance(item, dict) else str(item)
                            for item in output_content
                        ])
                    elif isinstance(output_content, str):
                        output_text = output_content
                    else:
                        output_text = str(output_content)
                    
                    # 将识别结果按行分割
                    if output_text:
                        lines = output_text.strip().split('\n')
                        
                        for line_idx, line in enumerate(lines):
                            if line.strip():
                                doc = Document(
                                    content=line.strip(),
                                    source=str(self.file_path),
                                    page=None,
                                    metadata={
                                        'confidence': 1.0,  # Qwen-VL 不返回单字置信度
                                        'line_index': line_idx,
                                        'type': 'qwen_vl_ocr',
                                        'model': self.model
                                    }
                                )
                                documents.append(doc)
            
            return documents
            
        except Exception as e:
            raise RuntimeError(f"OCR 识别失败：{e}")
    
    def parse_full_text(self) -> str:
        """识别并返回完整文字内容
        
        Returns:
            完整的识别文字字符串
        """
        docs = self.parse()
        return '\n'.join([doc.content for doc in docs])
    
    def parse_with_details(self) -> dict:
        """识别并返回详细信息
        
        Returns:
            包含完整信息的字典
        """
        self.validate_file()
        self._init_client()
        
        try:
            from dashscope import MultiModalConversation
            
            messages = [
                {
                    'role': 'user',
                    'content': [
                        {'image': str(self.file_path.absolute())},
                        {'text': '请识别图片中的所有文字内容'}
                    ]
                }
            ]
            
            response = self._client.call(
                model=self.model,
                messages=messages
            )
            
            if response and hasattr(response, 'output'):
                choices = response.output.get('choices', [])
                if choices and len(choices) > 0:
                    message = choices[0].get('message', {})
                    output_content = message.get('content', '')
                    
                    # output_content 可能是字符串或列表
                    if isinstance(output_content, list):
                        output_text = '\n'.join([
                            item.get('text', '') if isinstance(item, dict) else str(item)
                            for item in output_content
                        ])
                    elif isinstance(output_content, str):
                        output_text = output_content
                    else:
                        output_text = str(output_content)
                else:
                    output_text = ''
                
                return {
                    'success': True,
                    'text': output_text,
                    'request_id': getattr(response, 'request_id', None),
                    'usage': getattr(response, 'usage', None)
                }
            else:
                return {'success': False, 'error': 'No output'}
                
        except Exception as e:
            return {'success': False, 'error': str(e)}


async def create_qwen_vl_ocr_parser(
    image_path: Union[str, Path],
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest',
    language: str = 'zh'
) -> QwenVLOCRParser:
    """工厂函数：创建 Qwen-VL OCR 解析器实例
    
    Args:
        image_path: 图片路径
        api_key: 阿里云 API Key (可选)
        model: OCR 模型名称
        language: 识别语言
    
    Returns:
        QwenVLOCRParser 实例
    """
    return QwenVLOCRParser(
        file_path=image_path,
        api_key=api_key,
        model=model,
        language=language
    )
