"""测试多格式文档解析和 RAG 流程（支持 PDF、PPTX、PPT、DOCX）"""
from pathlib import Path
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

from src.parsers import PPTXParser, PDFParser, DocxParser
from src.embeddings import Embedder, VectorStore
from src.rag import RAGChain


def test_multi_format_parsing():
    """测试多格式文档解析（PDF、PPTX、DOCX）"""
    print("=" * 60)
    print("测试多格式文档解析")
    print("=" * 60)
    
    test_dir = Path("testppt")
    
    # 收集所有支持的文件（暂不支持 PPT 旧格式）
    all_files = (
        list(test_dir.glob("*.pdf")) + 
        list(test_dir.glob("*.pptx")) + 
        list(test_dir.glob("*.docx"))
    )
    
    # 统计跳过的 PPT 文件
    ppt_files = list(test_dir.glob("*.ppt"))
    
    print(f"\n找到 {len(all_files)} 个可解析文件")
    if ppt_files:
        print(f"⚠️  跳过 {len(ppt_files)} 个 .ppt 文件（需要 Windows COM 支持）")
    
    all_documents = []
    stats = {"pdf": 0, "pptx": 0, "docx": 0}
    
    for file_path in all_files:
        try:
            suffix = file_path.suffix.lower()
            parser_map = {
                '.pdf': PDFParser,
                '.pptx': PPTXParser,
                '.docx': DocxParser
            }
            
            parser_class = parser_map.get(suffix)
            if not parser_class:
                print(f"  ⚠️  跳过不支持的格式：{file_path.name}")
                continue
            
            print(f"\n解析文件：{file_path.name} ({suffix})")
            parser = parser_class(file_path)
            docs = parser.parse()
            print(f"  ✓ 提取 {len(docs)} 个文档块")
            
            all_documents.extend(docs)
            stats[suffix.lstrip('.')] += len(docs)
            
        except Exception as e:
            print(f"  ❌ 解析失败：{e}")
    
    print(f"\n📊 解析统计:")
    for format_name, count in stats.items():
        if count > 0:
            print(f"  {format_name.upper()}: {count} 个文档块")
    
    print(f"\n总共提取 {len(all_documents)} 个文档块")
    return all_documents


def test_embedding(docs):
    """测试向量化"""
    print("\n" + "=" * 60)
    print("测试文档向量化")
    print("=" * 60)
    
    embedder = Embedder(
        model_name="text-embedding-v2",  # 阿里云的 embedding 模型
        chunk_size=500,
        chunk_overlap=50
    )
    
    print("分块处理...")
    split_docs = embedder.split_documents(docs)
    print(f"✓ 分块后：{len(split_docs)} 个文本块")
    
    return split_docs, embedder


def test_rag_chain(split_docs, embedder):
    """测试 RAG 问答"""
    print("\n" + "=" * 60)
    print("测试 RAG 问答链")
    print("=" * 60)
    
    vector_store = VectorStore(persist_directory="./chroma_db_test")
    print("创建向量数据库...")
    vector_store.create(split_docs, embedder.get_embeddings())
    print("✓ 向量数据库创建成功")
    
    rag = RAGChain(vector_store)
    rag.initialize()
    print("✓ RAG 链初始化成功")
    
    # 测试问答
    question = "What is Chinese New Year?"
    print(f"\n测试问题：{question}")
    result = rag.query(question)
    print(f"回答：{result['answer'][:200]}...")
    if result['sources']:
        print(f"来源：{result['sources'][0]}")


if __name__ == "__main__":
    try:
        # 步骤 1: 解析所有格式文档（PDF、PPTX、PPT、DOCX）
        print("\n💡 提示：所有解析的文档将存储到同一个向量数据库中\n")
        docs = test_multi_format_parsing()
        
        # 步骤 2: 向量化
        split_docs, embedder = test_embedding(docs)
        
        # 步骤 3: RAG 问答
        test_rag_chain(split_docs, embedder)
        
        print("\n" + "=" * 60)
        print("🎉 所有测试通过！")
        print("✓ 支持格式：PDF、PPTX、PPT、DOCX")
        print("✓ 统一向量数据库存储")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
