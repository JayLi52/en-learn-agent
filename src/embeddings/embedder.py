"""文档向量化处理"""
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from src.parsers.base import Document


class Embedder:
    """文档向量化处理器"""

    def __init__(
        self,
        model_name: str = "text-embedding-3-small",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.embeddings = OpenAIEmbeddings(model=model_name)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """将文档分块"""
        from langchain.schema import Document as LCDocument

        lc_docs = [
            LCDocument(
                page_content=doc.content,
                metadata={
                    "source": doc.source,
                    **(doc.metadata or {}),
                }
            )
            for doc in documents
        ]

        split_docs = self.text_splitter.split_documents(lc_docs)

        return [
            Document(
                content=doc.page_content,
                source=doc.metadata.get("source", ""),
                metadata=doc.metadata,
            )
            for doc in split_docs
        ]

    def get_embeddings(self):
        """获取 embeddings 实例"""
        return self.embeddings