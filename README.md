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

## 安装

```bash
pip install -r requirements.txt
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