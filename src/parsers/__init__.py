"""文档解析模块

支持的解析器:
- PDFParser: 基于 pdfplumber 的 PDF 解析
- DocxParser: 基于 python-docx 的 Word 文档解析
- PPTXParser: 基于 python-pptx 的 PowerPoint 解析
- DoclingParser: 基于 Docling 的 AI 智能解析 (推荐，支持多格式统一处理)
- PaddleOCRParser: 基于 PaddleOCR 的图片文字识别 (纯本地离线，GPU 加速)
"""
from .base import BaseParser
from .pdf_parser import PDFParser
from .docx_parser import DocxParser
from .pptx_parser import PPTXParser

# 可选导入 Docling Parser
try:
    from .docling_parser import DoclingParser
    __all__ = ["BaseParser", "PDFParser", "DocxParser", "PPTXParser", "DoclingParser"]
except ImportError:
    # Docling 未安装时使用传统解析器
    __all__ = ["BaseParser", "PDFParser", "DocxParser", "PPTXParser"]

# 导入 PaddleOCR Parser
try:
    from .paddleocr_parser import PaddleOCRParser, create_paddle_ocr_parser
    from .paddleocr_model_manager import PaddleOCRModelManager, quick_setup_models
    __all__.extend(["PaddleOCRParser", "create_paddle_ocr_parser", "PaddleOCRModelManager", "quick_setup_models"])
except ImportError:
    # PaddleOCR 未安装时不暴露
    pass