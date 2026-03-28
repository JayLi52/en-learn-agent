# Qwen-VL OCR Skill

阿里云 Qwen-VL OCR 集成技能，提供高质量的图片文字识别能力。

## 功能特性

- ✅ 业界顶尖的 OCR 识别精度
- ✅ 支持复杂文档、表格、公式识别
- ✅ 支持手写体识别
- ✅ 多语言支持（中文、英文、自动检测）
- ✅ 批量处理能力
- ✅ 多种使用方式（Python API、命令行工具）

## 快速开始

### 1. 配置 API Key

在 `.env` 文件中设置:

```bash
DASHSCOPE_API_KEY=your_alibaba_api_key_here
```

获取 API Key: https://dashscope.console.aliyun.com/apiKey

### 2. Python 中使用

**简单识别:**
```python
from src.utils.qwen_vl_ocr import extract_text_from_image

text = extract_text_from_image('image.jpg')
print(text)
```

**批量处理:**
```python
from src.utils.qwen_vl_ocr import batch_extract_texts

results = batch_extract_texts(['img1.jpg', 'img2.png', 'img3.jpg'])
for result in results:
    if result['success']:
        print(f"{result['path']}: {result['text']}")
```

### 3. 命令行使用

**单张图片:**
```bash
python skills/qwen-ocr/scripts/qwen_ocr_quick.py image.jpg
```

**批量处理:**
```bash
python skills/qwen-ocr/scripts/qwen_ocr_batch.py ./images/ -o results.txt
```

## 文件结构

```
qwen-ocr/
├── SKILL.md                 # 主要技能文档
├── _meta.json              # 元数据
├── LICENSE.txt             # 许可证
├── scripts/                # 可执行脚本
│   ├── qwen_ocr_quick.py   # 快速识别脚本
│   └── qwen_ocr_batch.py   # 批量处理脚本
└── references/             # 参考资料
    └── api_reference.md    # API 参考文档
```

## 可用模型

| 模型 | 用途 | 精度 | 速度 |
|------|------|------|------|
| qwen-vl-ocr-latest | 通用场景 (推荐) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| qwen-vl-max | 高精度需求 | ⭐⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| qwen-vl-plus | 批量处理 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

## 使用示例

### 识别截图中的文字
```python
text = extract_text_from_image('screenshot.png')
```

### 识别表格并转为 CSV
```python
text = extract_text_from_image(
    'table.png',
    prompt='请按 CSV 格式还原图片中的表格内容'
)
```

### 识别数学公式
```python
text = extract_text_from_image(
    'formula.jpg',
    prompt='请用 LaTeX 格式识别图片中的数学公式'
)
```

### 批量扫描文档
```bash
python skills/qwen-ocr/scripts/qwen_ocr_batch.py ./scanned_pages/ --output book.txt
```

## 依赖

- Python 3.8+
- dashscope (阿里云 SDK)

安装依赖:
```bash
pip install dashscope
```

## 相关资源

- [完整技能文档](SKILL.md)
- [API 参考](references/api_reference.md)
- [阿里云官方文档](https://help.aliyun.com/zh/dashscope/)

## 许可证

Apache License 2.0
