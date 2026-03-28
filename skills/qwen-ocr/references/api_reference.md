# Qwen-VL OCR API 参考

## 模型对比

### qwen-vl-ocr-latest (推荐)
- **用途**: 通用场景，最佳平衡
- **精度**: 业界顶尖
- **速度**: 快
- **适用**: 文档、表格、公式、手写体混合场景

### qwen-vl-max
- **用途**: 高精度需求场景
- **精度**: 最高
- **速度**: 中等
- **适用**: 复杂版面、模糊图片、高难度识别

### qwen-vl-plus
- **用途**: 批量处理、成本敏感
- **精度**: 高
- **速度**: 最快
- **适用**: 简单文档、大批量处理

## 函数签名

### extract_text_from_image()

```python
def extract_text_from_image(
    image_path: Union[str, Path],
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest',
    prompt: str = '请准确完整地识别图片中的所有文字内容'
) -> str
```

**参数:**
- `image_path`: 图片路径
- `api_key`: 阿里云 API Key (可选)
- `model`: 模型名称
- `prompt`: 识别提示词

**返回:** 识别的文字内容

**异常:**
- `ValueError`: API Key 未设置
- `FileNotFoundError`: 图片文件不存在
- `RuntimeError`: 识别失败

---

### extract_text_with_details()

```python
def extract_text_with_details(
    image_path: Union[str, Path],
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest'
) -> dict
```

**返回字典:**
```python
{
    'success': bool,      # 是否成功
    'text': str,          # 识别的文字
    'request_id': str,    # 请求 ID
    'usage': dict,        # 用量信息
    'error': str          # 错误信息 (如果失败)
}
```

---

### batch_extract_texts()

```python
def batch_extract_texts(
    image_paths: list,
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest',
    verbose: bool = True
) -> list
```

**返回列表:**
```python
[
    {
        'path': str,       # 图片路径
        'text': str,       # 识别的文字
        'error': str,      # 错误信息
        'success': bool    # 是否成功
    }
]
```

---

### ocr() (便捷函数)

```python
def ocr(image_path: str, **kwargs) -> str
```

简洁调用方式:
```python
text = ocr('image.jpg')
```

## QwenVLOCRParser 类

### 构造函数

```python
QwenVLOCRParser(
    file_path: Union[str, Path],
    api_key: Optional[str] = None,
    model: str = 'qwen-vl-ocr-latest',
    language: str = 'zh'
)
```

**参数:**
- `file_path`: 图片文件路径
- `api_key`: API Key
- `model`: 模型名称
- `language`: 识别语言 ('zh', 'en', 'auto')

---

### parse()

```python
def parse() -> List[Document]
```

**返回:** Document 对象列表，每个包含:
- `content`: 文字内容
- `source`: 来源路径
- `metadata`: 
  - `confidence`: 置信度
  - `line_index`: 行索引
  - `type`: 'qwen_vl_ocr'
  - `model`: 使用的模型

---

### parse_full_text()

```python
def parse_full_text() -> str
```

**返回:** 完整的识别文字

---

### parse_with_details()

```python
def parse_with_details() -> dict
```

**返回:** 包含详细信息的字典

## 环境变量

### DASHSCOPE_API_KEY

阿里云 DashScope API Key

**获取方式:**
1. 访问 https://dashscope.console.aliyun.com/apiKey
2. 登录/注册阿里云账号
3. 创建或查看已有 API Key

**设置方法:**

Linux/Mac:
```bash
export DASHSCOPE_API_KEY=sk-your-key-here
```

Windows:
```cmd
set DASHSCOPE_API_KEY=sk-your-key-here
```

或在代码中传入:
```python
extract_text_from_image('image.jpg', api_key='sk-your-key-here')
```

## 典型使用场景

### 场景 1: 文档数字化

```python
from src.utils.qwen_vl_ocr import extract_text_from_image

text = extract_text_from_image('scanned_doc.jpg')
with open('digitized.txt', 'w', encoding='utf-8') as f:
    f.write(text)
```

### 场景 2: 表格识别

```python
text = extract_text_from_image(
    'table.png',
    prompt='请按 CSV 格式还原图片中的表格内容'
)
```

### 场景 3: 公式识别

```python
text = extract_text_from_image(
    'math_formula.jpg',
    prompt='请用 LaTeX 格式识别图片中的数学公式'
)
```

### 场景 4: 手写笔记

```python
text = extract_text_from_image(
    'handwritten_notes.jpg',
    prompt='请仔细识别手写笔记，尽量还原文字内容'
)
```

### 场景 5: 多语言混合

```python
text = extract_text_from_image(
    'mixed_lang.jpg',
    language='auto',
    prompt='请识别图片中的所有文字，保持原有的语言混合'
)
```

## 错误码参考

| 错误类型 | 说明 | 解决方案 |
|---------|------|---------|
| ValueError: 未找到 API Key | 环境变量未设置 | 设置 DASHSCOPE_API_KEY |
| FileNotFoundError | 图片不存在 | 检查文件路径 |
| RuntimeError: 网络错误 | API 调用失败 | 检查网络连接 |
| RuntimeError: API 返回为空 | 识别结果为空 | 尝试其他图片或模型 |

## 最佳实践

1. **选择合适的模型**: 根据精度和速度需求选择
2. **优化提示词**: 具体明确的提示能提高识别质量
3. **错误处理**: 始终检查 success 标志
4. **监控用量**: 定期查看 usage 了解消耗
5. **批量处理**: 多张图片使用 batch 接口更高效

## 相关链接

- [官方文档](https://help.aliyun.com/zh/dashscope/)
- [API 控制台](https://dashscope.console.aliyun.com/api)
- [定价说明](https://www.aliyun.com/product/dashscope)
