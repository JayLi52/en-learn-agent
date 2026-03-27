"""RAG 问答链"""
from typing import Optional
import os
from langchain_openai import ChatOpenAI
from langchain_core.runnables import Runnable
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate

from src.embeddings.vector_store import VectorStore
from src.embeddings.embedder import Embedder


PROMPT_TEMPLATE = """你是一个专业的英语教学助手。请根据以下上下文回答问题。
如果上下文中没有相关信息，请说明你不知道。

上下文：
{context}

问题：{question}

请用中文回答："""


class RAGChain:
    """RAG 问答链"""

    def __init__(
        self,
        vector_store: VectorStore,
        model_name: str = "qwen-plus",
        temperature: float = 0.7,
        api_base: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        self.vector_store = vector_store
        # 从环境变量或参数获取 API 配置
        self.api_base = api_base or os.getenv("BASE_URL")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        
        # 配置 LLM，支持 OpenAI 兼容 API
        llm_kwargs = {
            "model_name": model_name,
            "temperature": temperature,
        }
        if self.api_base:
            llm_kwargs["openai_api_base"] = self.api_base
        if self.api_key:
            llm_kwargs["openai_api_key"] = self.api_key
            
        self.llm = ChatOpenAI(**llm_kwargs)
        self._chain: Optional[Runnable] = None

    def initialize(self):
        """初始化 RAG 链"""
        # 使用相同的 API 配置初始化 Embedder
        embedder = Embedder(api_base=self.api_base, api_key=self.api_key)
        vectorstore = self.vector_store.load(embedder.get_embeddings())
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough
        
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

        # 使用新版本的 RAG chain 构建方式
        self._chain = (
            {"context": retriever | (lambda docs: "\n\n".join([d.page_content for d in docs])), 
             "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )

        return self._chain

    def query(self, question: str) -> dict:
        """执行问答"""
        if not self._chain:
            self.initialize()

        # 使用已经初始化的 chain 直接获取答案
        answer = self._chain.invoke(question)
        
        # 单独获取相关文档（用于显示来源）
        embedder = Embedder(api_base=self.api_base, api_key=self.api_key)
        vectorstore = self.vector_store.load(embedder.get_embeddings())
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
        docs = retriever.invoke(question)

        return {
            "answer": answer,
            "sources": [
                doc.metadata.get("source", "unknown")
                for doc in docs
            ]
        }