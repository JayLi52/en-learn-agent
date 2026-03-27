"""示例：启动交互式问答"""
import os
from dotenv import load_dotenv

from src.embeddings import VectorStore, Embedder
from src.rag import RAGChain


def interactive_qa(db_path: str = "./chroma_db"):
    """交互式问答"""
    load_dotenv()

    vector_store = VectorStore(persist_directory=db_path)
    rag = RAGChain(vector_store)
    rag.initialize()

    print("英语教学问答助手已启动 (输入 'quit' 退出)")
    print("-" * 50)

    while True:
        question = input("\n问题: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            break

        if not question:
            continue

        result = rag.query(question)
        print(f"\n回答: {result['answer']}")
        if result["sources"]:
            print(f"\n来源: {', '.join(set(result['sources']))}")


if __name__ == "__main__":
    interactive_qa()