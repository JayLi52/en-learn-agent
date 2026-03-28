# en-learn-agent

英语教学 AI Agent 项目

## 功能

- 文档向量化处理（支持 PDF、PPT、DOC）
- RAG 知识库问答系统

## 技术栈

- Python 3.10+
- LangChain - RAG 框架
- Chroma - 向量数据库
- OpenAI API - LLM & Embeddings
- **阿里云 Qwen-VL OCR - 云端 OCR(效果顶尖，强烈推荐)**
- ~~PaddleOCR~~ - 本地离线 OCR(可选，存在兼容性问题)

## 安装

```bash
pip install -r requirements.txt
```

### OCR 识别 (推荐：阿里云 Qwen-VL)

#### 🌟 推荐使用 - 阿里云 Qwen-VL OCR

**优势:**
- ✅ **识别效果业界顶尖** (qwen-vl-ocr-latest 模型)
- ✅ **云端 GPU 加速**,速度快 (1-3 秒)
- ✅ **无需本地模型**,不占资源
- ✅ **支持复杂文档**、表格、公式、手写体
- ✅ **与项目完美兼容**,无依赖冲突
- ✅ **简洁的函数接口**,易于使用

**快速开始:**

1. **获取 API Key**: https://dashscope.console.aliyun.com/apiKey

2. **配置环境变量**:
```bash
# 方式 1: 添加到 .env 文件
DASHSCOPE_API_KEY=your-api-key-here

# 方式 2: 终端临时设置
export DASHSCOPE_API_KEY=your-api-key-here
```

3. **在代码中使用**:
```python
from src.utils import extract_text_from_image

# 一行代码搞定!
text = extract_text_from_image('zuowen.jpg')
print(text)
```

4. **或使用命令行工具**:
```bash
python test_qwen_simple.py zuowen.jpg
```

**详细说明请查看**: [Qwen-VL OCR 使用指南](QWEN_VL_OCR_GUIDE.md)

---

#### 备选方案 - PaddleOCR (可选)

> ⚠️ **注意**: PaddleOCR 在 Mac 上存在兼容性问题，可能导致段错误或内存占用过高。
> 如无特殊需求，**强烈建议使用阿里云 Qwen-VL OCR**。

如需使用 PaddleOCR，请参考：[PaddleOCR 使用指南](PADDLEOCR_GUIDE.md)

## 使用

```bash
# 解析文档
python -m src.parsers.main --input /path/to/documents

# 启动问答
python -m src.rag.query
```

## 项目结构

```
src/
├── parsers/       # 文档解析器 (PDF, PPT, DOC)
├── embeddings/    # 向量化和存储
└── rag/          # RAG 问答链路
tests/            # 测试
docs/             # 文档
```

## 环境变量

创建 `.env` 文件：

```
OPENAI_API_KEY=your-api-key
```