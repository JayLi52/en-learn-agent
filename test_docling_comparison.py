"""对比测试：传统解析器 vs Docling 智能解析器"""
from pathlib import Path
import time
from dotenv import load_dotenv

load_dotenv()

# 测试两种解析方式
def test_traditional_parsers():
    """测试传统解析器（pdfplumber, python-pptx, python-docx）"""
    print("=" * 70)
    print("传统解析器测试")
    print("=" * 70)
    
    from src.parsers import PDFParser, PPTXParser, DocxParser
    
    test_dir = Path("testppt")
    all_docs = []
    
    # 测试 PDF
    pdf_files = list(test_dir.glob("*.pdf"))[:1]
    for pdf_file in pdf_files:
        try:
            print(f"\n解析 PDF: {pdf_file.name}")
            start = time.time()
            parser = PDFParser(pdf_file)
            docs = parser.parse()
            elapsed = time.time() - start
            print(f"  ✓ 提取 {len(docs)} 个文档块，耗时 {elapsed:.2f}s")
            all_docs.extend(docs)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
    
    # 测试 PPTX
    pptx_files = list(test_dir.glob("*.pptx"))[:2]
    for pptx_file in pptx_files:
        try:
            print(f"\n解析 PPTX: {pptx_file.name}")
            start = time.time()
            parser = PPTXParser(pptx_file)
            docs = parser.parse()
            elapsed = time.time() - start
            print(f"  ✓ 提取 {len(docs)} 个文档块，耗时 {elapsed:.2f}s")
            all_docs.extend(docs)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
    
    return all_docs


def test_docling_parser():
    """测试 Docling 智能解析器"""
    print("\n" + "=" * 70)
    print("Docling 智能解析器测试")
    print("=" * 70)
    
    try:
        from src.parsers import DoclingParser
    except ImportError:
        print("⚠️  Docling 未安装，跳过测试")
        print("安装指令：pip install docling")
        return []
    
    test_dir = Path("testppt")
    all_docs = []
    
    # 测试 PDF
    pdf_files = list(test_dir.glob("*.pdf"))[:1]
    for pdf_file in pdf_files:
        try:
            print(f"\n解析 PDF: {pdf_file.name} (使用 Docling)")
            start = time.time()
            parser = DoclingParser(pdf_file, export_format="markdown")
            docs = parser.parse()
            elapsed = time.time() - start
            
            # 获取文档信息
            info = parser.get_document_info()
            
            print(f"  ✓ 提取 {len(docs)} 个文档块")
            print(f"  📊 页数：{info.get('page_count', 'N/A')}")
            print(f"  ⏱️  耗时：{elapsed:.2f}s")
            print(f"  🎯 特性：{', '.join(info.get('supported_features', []))}")
            
            all_docs.extend(docs)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
    
    # 测试 PPTX
    pptx_files = list(test_dir.glob("*.pptx"))[:2]
    for pptx_file in pptx_files:
        try:
            print(f"\n解析 PPTX: {pptx_file.name} (使用 Docling)")
            start = time.time()
            parser = DoclingParser(pptx_file, export_format="markdown")
            docs = parser.parse()
            elapsed = time.time() - start
            
            info = parser.get_document_info()
            
            print(f"  ✓ 提取 {len(docs)} 个文档块")
            print(f"  📊 页数：{info.get('page_count', 'N/A')}")
            print(f"  ⏱️  耗时：{elapsed:.2f}s")
            print(f"  🎯 特性：{', '.join(info.get('supported_features', []))}")
            
            all_docs.extend(docs)
        except Exception as e:
            print(f"  ❌ 失败：{e}")
    
    return all_docs


def compare_results(traditional_docs, docling_docs):
    """对比结果"""
    print("\n" + "=" * 70)
    print("对比分析")
    print("=" * 70)
    
    print(f"\n📈 文档块数量:")
    print(f"  传统解析器：{len(traditional_docs)} 个")
    print(f"  Docling:     {len(docling_docs)} 个")
    
    if traditional_docs and docling_docs:
        avg_traditional = sum(len(doc.content) for doc in traditional_docs) / len(traditional_docs)
        avg_docling = sum(len(doc.content) for doc in docling_docs) / len(docling_docs)
        
        print(f"\n📝 平均文档长度:")
        print(f"  传统解析器：{avg_traditional:.0f} 字符")
        print(f"  Docling:     {avg_docling:.0f} 字符")
        
        print(f"\n💡 优势分析:")
        if docling_docs and len(docling_docs) > 0:
            print("  ✓ Docling 提供 AI 驱动的布局分析")
            print("  ✓ 自动识别阅读顺序")
            print("  ✓ 保留表格结构")
            print("  ✓ 统一的文档表示格式")
            print("  ✓ 支持更多文件格式")


if __name__ == "__main__":
    try:
        # 测试传统解析器
        traditional_docs = test_traditional_parsers()
        
        # 测试 Docling 解析器
        docling_docs = test_docling_parser()
        
        # 对比分析
        compare_results(traditional_docs, docling_docs)
        
        print("\n" + "=" * 70)
        print("✅ 测试完成！")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
