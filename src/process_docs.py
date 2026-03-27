"""示例：处理文档并创建向量索引"""
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv

from src.parsers import PDFParser, DocxParser, PPTXParser
from src.embeddings import Embedder, VectorStore


def get_parser(file_path: Path):
    """根据文件扩展名选择解析器"""
    suffix = file_path.suffix.lower()
    parsers = {
        ".pdf": PDFParser,
        ".docx": DocxParser,
        ".pptx": PPTXParser,
    }
    if suffix not in parsers:
        raise ValueError(f"不支持的文件格式: {suffix}")
    return parsers[suffix](file_path)


def process_directory(input_dir: str, output_db: str = "./chroma_db"):
    """处理目录下所有文档"""
    load_dotenv()

    input_path = Path(input_dir)
    all_documents = []

    # 支持的文件扩展名
    extensions = {".pdf", ".docx", ".pptx"}

    # 遍历目录
    for file_path in input_path.rglob("*"):
        if file_path.suffix.lower() in extensions:
            print(f"处理文件: {file_path}")
            parser = get_parser(file_path)
            documents = parser.parse()
            all_documents.extend(documents)
            print(f"  - 提取 {len(documents)} 个文档块")

    if not all_documents:
        print("未找到任何文档")
        return

    print(f"\n总共提取 {len(all_documents)} 个文档块")

    # 分块和向量化
    embedder = Embedder()
    split_docs = embedder.split_documents(all_documents)
    print(f"分块后: {len(split_docs)} 个文本块")

    # 存储到向量数据库
    vector_store = VectorStore(persist_directory=output_db)
    vector_store.create(split_docs, embedder.get_embeddings())
    print(f"\n向量数据库已保存到: {output_db}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="处理文档并创建向量索引")
    parser.add_argument("--input", "-i", required=True, help="文档目录路径")
    parser.add_argument("--output", "-o", default="./chroma_db", help="向量数据库输出路径")

    args = parser.parse_args()
    process_directory(args.input, args.output)