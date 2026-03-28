# Qwen-VL OCR 重构完成！

## ✅ 重构总结

已按照你的建议，将 Qwen-VL OCR **重构为简洁的工具函数**，不再使用复杂的 Parser 架构。

---

## 🎯 新的使用方式

### 方式一：在代码中使用 (推荐)

```python
from src.utils import extract_text_from_image

# 一行代码搞定!
text = extract_text_from_image('zuowen.jpg')
print(text)
```

### 方式二：命令行工具

```bash
python test_qwen_simple.py zuowen.jpg
```

---

## 📦 新文件结构

### 核心工具函数
```
src/utils/
└── qwen_vl_ocr.py    # OCR 工具函数模块
```

### 提供的函数

1. **`extract_text_from_image(image_path)`** 
   - 从图片提取文字
   - 返回字符串
   - 最常用!

2. **`extract_text_with_details(image_path)`**
   - 提取文字 + 详细信息
   - 返回字典 (包含 request_id, usage 等)

3. **`batch_extract_texts(image_paths)`**
   - 批量处理多个图片
   - 自动显示进度

4. **`ocr(image_path)`**
   - 便捷函数，更短的调用

---

## 💡 使用示例

### 基础使用

```python
from src.utils import extract_text_from_image

text = extract_text_from_image('zuowen.jpg')
print(f"识别结果：{text}")
```

### 自定义提示词

```python
# 可以要求模型按特定格式输出
text = extract_text_from_image(
    'homework.jpg',
    prompt='请识别学生的答案，只输出文字内容'
)
```

### 批量处理

```python
from pathlib import Path
from src.utils import batch_extract_texts

image_files = list(Path('images/').glob('*.jpg'))
results = batch_extract_texts(image_files)

for result in results:
    if result['success']:
        print(f"{result['path']}: {len(result['text'])}字")
    else:
        print(f"{result['path']}: 失败 - {result['error']}")
```

### 获取详细信息

```python
from src.utils import extract_text_with_details

result = extract_text_with_details('image.jpg')

if result['success']:
    print(f"文字：{result['text']}")
    print(f"Request ID: {result['request_id']}")
    print(f"用量：{result['usage']}")
```

---

## 🆚 对比旧版本

### ❌ 旧版本 (过度设计)

```python
from src.parsers import QwenVLOCRParser

parser = QwenVLOCRParser('image.jpg')
documents = parser.parse()
text = parser.parse_full_text()
```

### ✅ 新版本 (简洁直接)

```python
from src.utils import extract_text_from_image

text = extract_text_from_image('image.jpg')
```

**代码量减少 70%!**

---

## 🔧 API Key 配置

和之前一样，需要设置环境变量:

```bash
export DASHSCOPE_API_KEY=sk-your-key-here
```

或在 `.env` 文件中:

```
DASHSCOPE_API_KEY=sk-your-key-here
```

---

## 📁 文件变更

### 新增文件
- `src/utils/qwen_vl_ocr.py` - OCR 工具函数 (主要)
- `src/utils/__init__.py` - 工具模块导出
- `test_qwen_simple.py` - 简化版测试脚本

### 保留文件 (向后兼容)
- `src/parsers/qwen_vl_ocr_parser.py` - 旧 Parser (可选使用)
- `qwen_ocr.py` - 旧命令行工具 (可选使用)

---

## 🎉 优势

1. **接口简单** - 一个函数搞定
2. **易于理解** - 符合直觉的命名
3. **灵活使用** - 可以在任何地方调用
4. **无架构负担** - 不需要理解 Parser 模式
5. **更适合 LLM** - Qwen-VL 本身就是多模态模型，不需要封装成传统 OCR

---

## 🚀 立即试用

```bash
# 配置 API Key
export DASHSCOPE_API_KEY=sk-your-key

# 运行测试
python test_qwen_simple.py zuowen.jpg
```

或在代码中:

```python
from src.utils import ocr

text = ocr('zuowen.jpg')
print(text)
```

---

## 📚 详细文档

原有详细文档仍然有效:
- [QWEN_VL_OCR_GUIDE.md](QWEN_VL_OCR_GUIDE.md) - 完整使用指南
- [QWEN_OCR_QUICK_START.md](QWEN_OCR_QUICK_START.md) - 快速入门

---

## ✨ 总结

**听你的！这样简洁多了!** 😄

现在只需要:
1. 导入函数
2. 调用函数  
3. 拿到结果

就这么简单！🎉
