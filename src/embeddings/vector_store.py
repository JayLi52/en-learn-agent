"""向量数据库存储"""
from typing import List, Optional
from pathlib import Path
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document as LCDocument

from src.parsers.base import Document


class VectorStore:
    """Chroma 向量数据库管理"""

    def __init__(self, persist_directory: str = "./chroma_db"):
        self.persist_directory = Path(persist_directory)
        self._vectorstore: Optional[Chroma] = None

    def create(self, documents: List[Document], embeddings) -> Chroma:
        """创建向量存储"""
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

        self._vectorstore = Chroma.from_documents(
            documents=lc_docs,
            embedding=embeddings,
            persist_directory=str(self.persist_directory),
        )

        return self._vectorstore

    def load(self, embeddings) -> Chroma:
        """加载已有向量存储"""
        self._vectorstore = Chroma(
            persist_directory=str(self.persist_directory),
            embedding_function=embeddings,
        )
        return self._vectorstore

    def add_documents(self, documents: List[Document]) -> None:
        """添加新文档到向量存储"""
        if not self._vectorstore:
            raise RuntimeError("向量存储未初始化，请先调用 create() 或 load()")

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

        self._vectorstore.add_documents(lc_docs)

    def get_retriever(self, k: int = 4):
        """获取检索器"""
        if not self._vectorstore:
            raise RuntimeError("向量存储未初始化")
        return self._vectorstore.as_retriever(search_kwargs={"k": k})