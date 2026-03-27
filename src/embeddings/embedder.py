"""文档向量化处理"""
from typing import List, Optional
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.parsers.base import Document


class Embedder:
    """文档向量化处理器"""

    def __init__(
        self,
        model_name: str = "text-embedding-v2",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        # 从环境变量或参数获取 API 配置
        self.api_base = api_base or os.getenv("BASE_URL")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # 确保有 API key
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY 未设置，请传入 api_key 参数或设置 OPENAI_API_KEY 环境变量")
        
        # 检测是否是阿里云 DashScope
        is_dashscope = self.api_base and ("dashscope" in self.api_base or "aliyuncs" in self.api_base)
        
        if is_dashscope:
            # 使用阿里云 DashScope SDK
            try:
                import dashscope
                from dashscope import TextEmbedding
                
                dashscope.api_key = self.api_key
                self.model_name = "text-embedding-v2"
                self.use_dashscope = True
            except ImportError:
                print("警告：dashscope 未安装，将尝试使用 OpenAI 兼容模式")
                self.use_dashscope = False
        else:
            self.use_dashscope = False
            from langchain_openai import OpenAIEmbeddings
            self.embeddings = OpenAIEmbeddings(
                model=model_name,
                api_key=self.api_key,
                openai_api_base=self.api_base
            )
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """将文档分块"""
        from langchain_core.documents import Document as LCDocument

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
        if self.use_dashscope:
            # 返回一个适配器对象
            return DashScopeEmbeddingAdapter(self.api_key, self.model_name)
        return self.embeddings


class DashScopeEmbeddingAdapter:
    """DashScope Embeddings 适配器，用于兼容 LangChain"""
    
    def __init__(self, api_key: str, model: str = "text-embedding-v2"):
        self.api_key = api_key
        self.model = model
        
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """批量获取 embeddings"""
        import dashscope
        from dashscope import TextEmbedding
        
        dashscope.api_key = self.api_key
        
        results = []
        for text in texts:
            # 确保 text 是字符串
            if not isinstance(text, str):
                text = str(text)
            
            # 阿里云 API：单个文本直接传字符串
            response = TextEmbedding.call(
                model=self.model,
                input=text
            )
            
            if response.status_code == 200:
                embedding = response.output['embeddings'][0]['embedding']
                results.append(embedding)
            else:
                raise Exception(f"Error getting embedding: {response}")
        
        return results
    
    def embed_query(self, text: str) -> List[float]:
        """获取单个查询的 embedding"""
        return self.embed_documents([text])[0]