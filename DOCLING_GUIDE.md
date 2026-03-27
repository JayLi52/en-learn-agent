# Docling 智能文档解析器集成指南

## 📦 什么是 Docling？

[Docling](https://github.com/docling-project/docling) 是一个强大的 AI 驱动文档解析工具，提供：

### 核心优势
- **AI 驱动的布局分析** - 理解文档结构，识别标题、段落、表格等
- **阅读顺序检测** - 自动识别正确的阅读顺序（特别是多栏文档）
- **表格结构保留** - 完整保留表格的行列结构和内容
- **统一文档表示** - 将不同格式转换为统一的 `DoclingDocument` 结构
- **多格式支持** - PDF、DOCX、PPTX、HTML、图片等

### 支持的格式

| 格式 | 扩展名 | 后端实现 |
|------|--------|----------|
| **PDF** | `.pdf` | `DoclingParseDocumentBackend`, `PyPdfiumDocumentBackend` |
| **DOCX** | `.docx`, `.dotx`, `.docm`, `.dotm` | `MsWordDocumentBackend` |
| **PPTX** | `.pptx`, `.potx`, `.ppsx`, `.pptm`, `.potm`, `.ppsm` | `MsPowerpointDocumentBackend` |
| **HTML** | `.html`, `.htm` | HTML 解析器 |
| **图片** | `.png`, `.jpg`, `.jpeg`, `.tiff` | OCR + 图像分析 |

---

## 🚀 快速开始

### 1. 安装 Docling

```bash
# 基础安装（推荐）
pip install docling

# 或者从 requirements.txt 安装
pip install -r requirements.txt
```

**注意**: Docling 首次安装可能需要较长时间（约 5-10 分钟），因为需要编译 docling-parse 组件。

### 2. 使用示例

#### 简单用法（5 行代码）

```python
from pathlib import Path
from src.parsers import DoclingParser

# 解析 PDF 文件
parser = DoclingParser(Path("document.pdf"))
docs = parser.parse()

print(f"提取了 {len(docs)} 个文档块")
print(f"内容预览：{docs[0].content[:200]}...")
```

#### 导出不同格式

```python
# Markdown 格式（推荐用于 RAG）
parser_md = DoclingParser(file_path, export_format="markdown")

# JSON 格式（完整结构化数据）
parser_json = DoclingParser(file_path, export_format="json")

# HTML 格式（保留样式）
parser_html = DoclingParser(file_path, export_format="html")
```

---

## 🔬 技术细节

### DoclingParser 类结构

```python
class DoclingParser(BaseParser):
    """
    使用 Docling 进行智能文档解析
    
    参数:
        file_path: 文件路径 (Path 对象)
        export_format: 导出格式 ("markdown", "json", "html", "text")
    
    方法:
        parse() -> List[Document]: 解析文档返回 Document 列表
        get_document_info() -> dict: 获取文档元信息
    """
```

### 工作流程

```
文件输入 → Docling 转换 → AI 布局分析 → 结构化表示 → 导出格式化 → Document 对象
                ↓
         阅读顺序检测
         表格识别
         层次结构分析
```

### Document 对象

每个 Document 包含：
- `content`: 文本内容（Markdown/JSON/HTML 等格式）
- `source`: 源文件路径
- `page`: 页码
- `metadata`: 元数据（文件格式、解析器类型、特性等）

---

## 📊 对比测试

### 传统解析器 vs Docling

我们提供了对比测试脚本：

```bash
# 运行对比测试
python test_docling_comparison.py
```

### 预期结果

| 指标 | 传统解析器 | Docling |
|------|-----------|---------|
| **PDF 解析** | 基于规则，简单文本提取 | AI 理解布局，保留结构 |
| **PPTX 解析** | 文本框拼接 | 幻灯片结构化，保留层次 |
| **表格处理** | ❌ 不支持或丢失格式 | ✅ 完整保留表格结构 |
| **阅读顺序** | ❌ 可能错乱 | ✅ 自动识别正确顺序 |
| **多栏文档** | ❌ 难以处理 | ✅ 正确分栏和排序 |
| **解析速度** | ⚡️ 快（秒级） | 🐢 较慢（数十秒） |
| **准确性** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 💡 实际应用场景

### 场景 1: RAG 知识库构建

```python
from src.parsers import DoclingParser
from src.embeddings import Embedder, VectorStore
from src.rag import RAGChain

# 1. 解析文档
parser = DoclingParser(Path("manual.pdf"), export_format="markdown")
docs = parser.parse()

# 2. 向量化
embedder = Embedder(chunk_size=500, chunk_overlap=50)
split_docs = embedder.split_documents(docs)

# 3. 存储到向量数据库
vector_store = VectorStore(persist_directory="./chroma_db")
vector_store.create(split_docs, embedder.get_embeddings())

# 4. RAG 问答
rag = RAGChain(vector_store)
rag.initialize()
result = rag.query("如何配置系统？")
print(result['answer'])
```

### 场景 2: 批量文档处理

```python
from pathlib import Path
from src.parsers import DoclingParser

test_dir = Path("documents")
all_docs = []

# 批量解析多种格式
for file_path in test_dir.glob("*"):
    if file_path.suffix in ['.pdf', '.docx', '.pptx']:
        print(f"解析：{file_path.name}")
        parser = DoclingParser(file_path)
        docs = parser.parse()
        all_docs.extend(docs)

print(f"总共提取 {len(all_docs)} 个文档块")
```

### 场景 3: 表格数据提取

```python
parser = DoclingParser(Path("financial_report.xlsx"), export_format="json")
docs = parser.parse()

import json
data = json.loads(docs[0].content)
# data 包含完整的表格结构和数据
```

---

## ⚙️ 高级配置

### 性能优化

```python
# GPU 加速（如果有 NVIDIA GPU）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Apple Silicon 加速（M1/M2/M3 Mac）
# Docling 会自动使用 MLX 框架加速
```

### OCR 配置（处理扫描版 PDF）

```bash
# 安装 Tesseract OCR
# macOS
brew install tesseract leptonica pkg-config
export TESSDATA_PREFIX=/opt/homebrew/share/tessdata/

# Ubuntu/Debian
apt-get install tesseract-ocr tesseract-ocr-eng libtesseract-dev libleptonica-dev pkg-config
```

---

## 🔍 故障排查

### 问题 1: 导入错误

```python
ImportError: cannot import name 'DoclingParser' from 'src.parsers'
```

**解决方案**: Docling 未安装成功
```bash
pip install docling
# 或检查 requirements.txt
pip install -r requirements.txt
```

### 问题 2: 解析速度慢

**原因**: AI 模型需要推理时间
**解决方案**: 
- 使用批量处理减少初始化开销
- 考虑 GPU 加速
- 对于简单文档使用传统解析器

### 问题 3: 内存占用高

Docling 加载 AI 模型需要较多内存（约 2-4GB）
**解决方案**:
- 减少并发处理数量
- 使用较小的 batch size
- 考虑使用传统解析器处理简单文档

---

## 📈 未来规划

### 即将支持的功能
- [ ] 元数据提取（标题、作者、参考文献、语言）
- [ ] 视觉语言模型集成（SmolDocling）
- [ ] 图表理解（柱状图、饼图、折线图等）
- [ ] 复杂化学物质识别（分子结构）
- [ ] 公式识别和 LaTeX 导出

### 集成计划
- [ ] LangChain 深度集成
- [ ] LlamaIndex 连接器
- [ ] Haystack 组件
- [ ] CrewAI 工具

---

## 📚 参考资源

- **GitHub**: https://github.com/docling-project/docling
- **官方文档**: https://docling-project.github.io/
- **Quick Start**: https://docling-project.github.io/docling/quick_start/
- **API 参考**: https://docling-project.github.io/docling/reference/

---

## 🎯 总结

### 何时使用 Docling？

✅ **推荐使用**:
- 复杂排版的 PDF 文档（论文、报告、手册）
- 包含表格的文档
- 多栏布局的文档
- 需要精确阅读顺序的场景
- 混合多种文件格式的处理

❌ **不推荐**:
- 简单的纯文本文档（用传统解析器更快）
- 对处理速度要求极高的场景
- 内存受限的环境

### 最佳实践

1. **选择合适的导出格式**: RAG 场景用 Markdown，数据处理用 JSON
2. **批量处理**: 一次性处理多个文档减少初始化开销
3. **混合使用**: 根据文档类型选择解析器（简单文档用传统，复杂文档用 Docling）
4. **缓存结果**: 解析后的文档可以序列化保存，避免重复处理

---

*最后更新：2026 年 3 月 27 日*
