# Qwen-VL OCR 快速使用指南

## 🎯 三步开始识别

### 步骤 1: 获取 API Key

访问：https://dashscope.console.aliyun.com/apiKey

1. 登录阿里云账号 (没有就注册一个)
2. 开通 DashScope 服务 (免费)
3. 创建或查看 API Key (格式：`sk-xxxxxxxx`)

### 步骤 2: 配置 API Key

**推荐方式**:添加到 `.env` 文件

在项目根目录创建 `.env` 文件:

```bash
DASHSCOPE_API_KEY=sk-你的 api-key-here
```

### 步骤 3: 开始识别

```bash
python qwen_ocr.py zuowen.jpg
```

---

## 💻 代码示例

### 基础使用

```python
from src.parsers import QwenVLOCRParser

parser = QwenVLOCRParser(
    file_path='zuowen.jpg',
    model='qwen-vl-ocr-latest'
)

# 识别并获取结果
documents = parser.parse()
for doc in documents:
    print(doc.content)
```

### 获取完整文本

```python
full_text = parser.parse_full_text()
print(full_text)
```

---

## ✨ 核心优势

- ✅ **识别效果顶尖** - qwen-vl-ocr-latest 模型
- ✅ **云端 GPU 加速** - 1-3 秒完成
- ✅ **零资源占用** - 所有计算在云端
- ✅ **完美兼容性** - 无依赖冲突
- ✅ **支持复杂场景** - 表格、公式、手写体

---

## 💰 费用说明

- 新用户有免费额度
- 约 0.007 元/次
- 查询用量：https://dashscope.console.aliyun.com/usage

---

## 🔧 常见问题

### Q: API Key 在哪里获取？
A: https://dashscope.console.aliyun.com/apiKey

### Q: 需要联网吗？
A: 是的，需要联网调用云端 API

### Q: 支持哪些图片格式？
A: JPG, PNG, BMP, WEBP, PDF

### Q: 如何批量处理？
```python
from pathlib import Path
from src.parsers import QwenVLOCRParser

for img in Path('images/').glob('*.jpg'):
    parser = QwenVLOCRParser(img)
    text = parser.parse_full_text()
    print(f"{img.name}: {len(text)}字")
```

---

## 📚 详细文档

查看 [QWEN_VL_OCR_GUIDE.md](QWEN_VL_OCR_GUIDE.md) 了解更多高级用法。
