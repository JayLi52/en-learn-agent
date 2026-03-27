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
- **PaddleOCR - 本地离线 OCR(支持 Mac GPU 加速)**

## 安装

```bash
pip install -r requirements.txt
```

### PaddleOCR 特别说明

本项目集成了 **PaddleOCR PP-OCRv5** 轻量级 OCR 能力:
- ✅ **纯本地离线运行**,无需联网
- ✅ **自动调用 Mac GPU(Metal)** 加速 (M1/M2/M3/M4)
- ✅ **中英文混合识别**,准确率 99%+
- ✅ **倾斜文字自动修正**

#### 首次使用配置模型 (可选，仅第一次需要)

```bash
# 方式 1: 自动下载默认模型 (首次运行时自动下载)
python quick_ocr.py

# 方式 2: 手动下载 PP-OCRv5 最优模型到指定位置
python -m src.parsers.paddleocr_model_manager ~/paddleocr_models
```

#### 使用 PaddleOCR

```bash
# 快速识别图片文字
python quick_ocr.py test.jpg

# 使用本地离线模型
python quick_ocr.py test.jpg ~/Desktop/paddle_ocr/models

# 验证安装
python -m scripts.verify_paddle_install
```

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