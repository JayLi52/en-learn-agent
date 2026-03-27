"""解析器基类"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Union
from pathlib import Path


@dataclass
class Document:
    """解析后的文档结构"""
    content: str
    source: str
    page: Optional[int] = None
    metadata: Optional[dict] = None


class BaseParser(ABC):
    """文档解析器基类"""

    def __init__(self, file_path: Union[str, Path]):
        self.file_path = Path(file_path)

    @abstractmethod
    def parse(self) -> List[Document]:
        """解析文档，返回文档块列表"""
        pass

    def validate_file(self) -> bool:
        """验证文件是否存在且格式正确"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"文件不存在: {self.file_path}")
        return True