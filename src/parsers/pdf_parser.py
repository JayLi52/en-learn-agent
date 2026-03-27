"""PDF 文档解析器"""
from typing import List
from pathlib import Path
from .base import BaseParser, Document


class PDFParser(BaseParser):
    """解析 PDF 文档"""

    def parse(self) -> List[Document]:
        self.validate_file()
        documents = []

        # 使用 PyMuPDF 解析
        import fitz  # PyMuPDF

        with fitz.open(self.file_path) as doc:
            for page_num, page in enumerate(doc, 1):
                text = page.get_text()
                if text.strip():
                    documents.append(Document(
                        content=text,
                        source=str(self.file_path),
                        page=page_num,
                        metadata={
                            "file_type": "pdf",
                            "page": page_num,
                        }
                    ))

        return documents