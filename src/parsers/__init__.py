"""文档解析模块"""
from .base import BaseParser
from .pdf_parser import PDFParser
from .docx_parser import DocxParser
from .pptx_parser import PPTXParser

__all__ = ["BaseParser", "PDFParser", "DocxParser", "PPTXParser"]