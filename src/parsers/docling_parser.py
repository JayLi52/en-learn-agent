"""Docling 通用文档解析器 - 支持 PDF、DOCX、PPTX 统一解析"""
from typing import List, Optional
from pathlib import Path
from .base import BaseParser, Document


class DoclingParser(BaseParser):
    """
    使用 Docling 进行智能文档解析
    
    优势:
    - AI 驱动的布局分析，理解文档结构
    - 表格结构识别和保留
    - 阅读顺序检测
    - 统一的文档表示
    - 支持 PDF、DOCX、PPTX、HTML、图片等格式
    
    参考：https://github.com/docling-project/docling
    """
    
    def __init__(self, file_path: Path, export_format: str = "markdown"):
        """
        初始化 Docling 解析器
        
        Args:
            file_path: 文件路径
            export_format: 导出格式 ("markdown", "json", "html", "text")
                          - markdown: 人类可读，适合 RAG (推荐)
                          - json: 完整结构化数据，适合进一步处理
                          - html: 保留样式
                          - text: 纯文本
        """
        super().__init__(file_path)
        self.export_format = export_format
        self.converter = None
    
    def _init_converter(self):
        """延迟初始化转换器"""
        try:
            from docling.document_converter import DocumentConverter
            from docling.datamodel.base_models import OutputFormat
            
            # 配置输出格式
            if self.export_format == "markdown":
                output_format = OutputFormat.MARKDOWN
            elif self.export_format == "json":
                output_format = OutputFormat.JSON
            elif self.export_format == "html":
                output_format = OutputFormat.HTML
            else:
                output_format = OutputFormat.TEXT
            
            self.converter = DocumentConverter()
            self.output_format = output_format
            
        except ImportError as e:
            raise ImportError(
                "Docling 未安装！请运行：pip install docling\n"
                "详细说明：https://github.com/docling-project/docling"
            ) from e
    
    def parse(self) -> List[Document]:
        """
        使用 Docling 解析文档
        
        Returns:
            Document 列表，包含解析后的内容
        """
        self.validate_file()
        
        # 初始化转换器（延迟加载）
        if not self.converter:
            self._init_converter()
        
        try:
            # 转换文档
            result = self.converter.convert(str(self.file_path))
            
            # 根据格式导出
            if self.export_format == "markdown":
                content = result.document.export_to_markdown()
            elif self.export_format == "json":
                import json
                content = json.dumps(result.document.export_to_dict(), ensure_ascii=False)
            elif self.export_format == "html":
                content = result.document.export_to_html()
            else:
                content = result.document.export_to_text()
            
            # 创建 Document 对象
            # Docling 已经做了很好的分块和结构化，我们按页面或逻辑块分割
            documents = []
            
            # 尝试按页面分割（如果有页码信息）
            if hasattr(result, 'pages') and result.pages:
                for page_num, page in enumerate(result.pages, 1):
                    # 提取每页的内容
                    page_content = self._extract_page_content(page)
                    if page_content.strip():
                        documents.append(Document(
                            content=page_content,
                            source=str(self.file_path),
                            page=page_num,
                            metadata={
                                "file_type": self.file_path.suffix.lower(),
                                "parser": "docling",
                                "format": self.export_format,
                            }
                        ))
            else:
                # 如果没有分页信息，作为单个文档
                if content.strip():
                    documents.append(Document(
                        content=content,
                        source=str(self.file_path),
                        page=1,
                        metadata={
                            "file_type": self.file_path.suffix.lower(),
                            "parser": "docling",
                            "format": self.export_format,
                            "total_pages": getattr(result, 'page_count', 1),
                        }
                    ))
            
            return documents
            
        except Exception as e:
            raise RuntimeError(f"Docling 解析失败：{e}") from e
    
    def _extract_page_content(self, page) -> str:
        """
        从页面提取内容
        
        Args:
            page: Docling 页面对象
            
        Returns:
            页面文本内容
        """
        # 尝试获取 markdown 表示
        try:
            if hasattr(page, 'export_to_markdown'):
                return page.export_to_markdown()
        except:
            pass
        
        # 回退到基础文本提取
        texts = []
        if hasattr(page, 'cells'):
            for cell in page.cells:
                if hasattr(cell, 'text') and cell.text:
                    texts.append(cell.text)
        
        return "\n\n".join(texts) if texts else ""
    
    def get_document_info(self) -> dict:
        """
        获取文档元信息
        
        Returns:
            包含页数、格式等信息的字典
        """
        if not self.converter:
            self._init_converter()
        
        try:
            result = self.converter.convert(str(self.file_path))
            return {
                "file_type": self.file_path.suffix.lower(),
                "page_count": result.page_count if hasattr(result, 'page_count') else 1,
                "parser": "docling",
                "supported_features": [
                    "layout_analysis",
                    "table_structure",
                    "reading_order",
                    "multi_format",
                ]
            }
        except Exception as e:
            return {
                "error": str(e),
                "file_type": self.file_path.suffix.lower(),
            }
