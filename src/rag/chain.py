"""RAG 问答链"""
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

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
        model_name: str = "gpt-4o-mini",
        temperature: float = 0.7,
    ):
        self.vector_store = vector_store
        self.embedder = Embedder()
        self.llm = ChatOpenAI(
            model_name=model_name,
            temperature=temperature,
        )
        self._chain: Optional[RetrievalQA] = None

    def initialize(self):
        """初始化 RAG 链"""
        vectorstore = self.vector_store.load(self.embedder.get_embeddings())
        retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "question"]
        )

        self._chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt},
        )

        return self._chain

    def query(self, question: str) -> dict:
        """执行问答"""
        if not self._chain:
            self.initialize()

        result = self._chain.invoke({"query": question})

        return {
            "answer": result["result"],
            "sources": [
                doc.metadata.get("source", "unknown")
                for doc in result.get("source_documents", [])
            ]
        }