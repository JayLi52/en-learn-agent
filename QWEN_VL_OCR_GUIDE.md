# 阿里云 Qwen-VL OCR 集成指南

## 🚀 快速开始

### 1. 获取 API Key

访问阿里云 DashScope 控制台获取 API Key:
https://dashscope.console.aliyun.com/apiKey

### 2. 配置环境变量

**方式一：添加到 .env 文件 (推荐)**

在项目根目录的 `.env` 文件中添加:

```bash
DASHSCOPE_API_KEY=your-api-key-here
```

**方式二：终端临时设置**

```bash
export DASHSCOPE_API_KEY=your-api-key-here
```

### 3. 安装依赖

```bash
pip install dashscope
```

---

## 💡 使用方法

### 方式一：快速识别脚本

```bash
python qwen_ocr.py zuowen.jpg
```

### 方式二：在代码中使用

```python
from src.parsers import QwenVLOCRParser

# 创建解析器
parser = QwenVLOCRParser(
    file_path='zuowen.jpg',
    model='qwen-vl-ocr-latest',
    language='auto'  # 自动检测语言
)

# 执行识别
documents = parser.parse()

for doc in documents:
    print(f"文字：{doc.content} | 置信度：{doc.metadata['confidence']:.2f}")

# 获取完整文本
full_text = parser.parse_full_text()
print(full_text)
```

### 方式三：异步工厂方法

```python
from src.parsers import create_qwen_vl_ocr_parser

parser = await create_qwen_vl_ocr_parser(
    image_path='zuowen.jpg',
    model='qwen-vl-ocr-latest',
    language='zh'
)

result = parser.parse_full_text()
```

---

## 📊 技术规格

### 使用模型
- **qwen-vl-ocr-latest** - 阿里云最新最强的 OCR 模型

### 支持的语言
- `'zh'` - 中文
- `'en'` - 英文
- `'auto'` - 自动检测 (推荐)

### 支持的图片格式
- JPG/JPEG
- PNG
- BMP
- WEBP
- PDF (多页文档)

### 核心特性
- ✅ **业界顶尖识别率** - 中文 OCR 准确率 99%+
- ✅ **复杂文档处理** - 支持表格、公式、图表混排
- ✅ **手写体识别** - 支持常见手写字体
- ✅ **云端 GPU 加速** - 识别速度快，通常 1-3 秒
- ✅ **无需本地模型** - 不占用本地资源
- ✅ **自动语言检测** - 智能识别中英文混合

---

## 🔧 高级用法

### 获取详细识别信息

```python
parser = QwenVLOCRParser('image.jpg')
details = parser.parse_with_details()

if details['success']:
    content = details['content']
    for item in content:
        print(f"文字：{item['text']}")
        print(f"置信度：{item.get('confidence', 0):.2f}")
        print(f"位置：{item.get('position', 'N/A')}")
        print()
```

### 指定特定语言

```python
# 纯中文文档
parser = QwenVLOCRParser('chinese.jpg', language='zh')

# 纯英文文档
parser = QwenVLOCRParser('english.jpg', language='en')

# 中英混合或未知语言
parser = QwenVLOCRParser('mixed.jpg', language='auto')
```

### 批量处理

```python
from pathlib import Path
from src.parsers import QwenVLOCRParser

image_files = list(Path('images/').glob('*.jpg'))

for img_path in image_files:
    try:
        parser = QwenVLOCRParser(img_path)
        text = parser.parse_full_text()
        print(f"{img_path.name}: {len(text)} 字")
    except Exception as e:
        print(f"识别失败 {img_path.name}: {e}")
```

---

## 💰 费用说明

### 免费额度
- 新用户注册即送免费额度
- 具体额度请查看官网

### 计费标准
- 按调用次数计费
- 约 0.007 元/次 (价格可能变动，以官网为准)
- 量大从优

### 查询用量
登录 DashScope 控制台查看用量统计:
https://dashscope.console.aliyun.com/usage

---

## ⚠️ 注意事项

### API Key 安全
- ❌ 不要将 API Key 提交到 Git 仓库
- ✅ 使用 `.env` 文件管理 (已添加到 `.gitignore`)
- ✅ 定期更换 API Key
- ✅ 设置合理的调用限额

### 网络要求
- 需要联网才能使用
- 首次调用可能需要 1-2 秒建立连接
- 建议添加超时和重试机制

### 错误处理

```python
try:
    parser = QwenVLOCRParser('image.jpg')
    result = parser.parse()
except ValueError as e:
    # API Key 未设置
    print(f"配置错误：{e}")
except RuntimeError as e:
    # 识别失败
    print(f"识别错误：{e}")
except Exception as e:
    # 其他错误
    print(f"未知错误：{e}")
```

---

## 🆚 与 PaddleOCR 对比

| 特性 | Qwen-VL OCR (推荐) | PaddleOCR |
|------|-------------------|-----------|
| **识别效果** | ⭐⭐⭐⭐⭐ 顶尖 | ⭐⭐⭐⭐ 优秀 |
| **速度** | ⭐⭐⭐⭐⭐ 1-3 秒 | ⭐⭐⭐ 5-10 秒 (首次更慢) |
| **资源占用** | ⭐⭐⭐⭐⭐ 云端 | ⭐⭐⭐ 本地 200MB+ |
| **离线使用** | ❌ 需联网 | ✅ 可离线 |
| **成本** | 💰 按次计费 | 💰 免费 |
| **复杂度** | ⭐⭐⭐⭐⭐ 简单 | ⭐⭐ 复杂 |
| **兼容性** | ⭐⭐⭐⭐⭐ 完美 | ⭐⭐⭐ 有兼容问题 |

**推荐使用场景:**
- ✅ **Qwen-VL OCR**: 生产环境、追求最佳效果、快速部署
- ✅ **PaddleOCR**: 离线环境、大量批量处理、成本敏感

---

## 🎉 总结

阿里云 Qwen-VL OCR (`qwen-vl-ocr-latest`) 已经集成完成！

现在你的项目具备:
- ✅ **业界顶尖的 OCR 识别能力**
- ✅ **云端 GPU 加速，速度快**
- ✅ **无需担心本地兼容性问题**
- ✅ **支持复杂文档、表格、公式、手写体**

立即开始使用:
```bash
python qwen_ocr.py zuowen.jpg
```
