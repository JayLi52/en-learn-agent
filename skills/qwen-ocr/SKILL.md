---
name: qwen-ocr
description: Use Alibaba's Qwen-VL OCR for high-quality text extraction from images. Supports complex documents, tables, formulas, and handwritten text recognition. Provides both simple text extraction and detailed API responses with usage information.
license: Complete terms in LICENSE.txt
---

# Qwen-VL OCR

Use Alibaba Cloud's Qwen-VL OCR service to extract text from images with industry-leading accuracy. This skill supports complex documents, tables, formulas, charts, and handwritten text.

## When to Use

Use this skill when users need to:
- Extract text from images (screenshots, photos, scanned documents)
- Recognize text in complex layouts (tables, formulas, diagrams)
- Handle handwritten content
- Process multi-language content (Chinese, English, auto-detection)
- Get OCR results with high accuracy requirements

## Setup Requirements

### Environment Variable

Set `DASHSCOPE_API_KEY` in your `.env` file:

```bash
DASHSCOPE_API_KEY=your_alibaba_api_key_here
```

Get your API key from: https://dashscope.console.aliyun.com/apiKey

### Python Dependencies

Ensure these are installed:
```bash
pip install dashscope
```

## Usage Methods

### Method 1: Simple Text Extraction (Recommended)

For most use cases - returns extracted text directly:

```python
from src.utils.qwen_vl_ocr import extract_text_from_image

text = extract_text_from_image('path/to/image.jpg')
print(text)
```

**With custom prompt:**
```python
text = extract_text_from_image(
    'image.jpg',
    prompt='请只识别图片中的标题文字'
)
```

### Method 2: Detailed Response

When you need request metadata and usage information:

```python
from src.utils.qwen_vl_ocr import extract_text_with_details

result = extract_text_with_details('path/to/image.jpg')

if result['success']:
    print(f"Text: {result['text']}")
    print(f"Request ID: {result['request_id']}")
    print(f"Usage: {result['usage']}")
else:
    print(f"Error: {result['error']}")
```

### Method 3: Batch Processing

Process multiple images at once:

```python
from src.utils.qwen_vl_ocr import batch_extract_texts

image_paths = ['img1.jpg', 'img2.png', 'img3.jpg']
results = batch_extract_texts(image_paths)

for result in results:
    if result['success']:
        print(f"{result['path']}: {result['text']}")
    else:
        print(f"{result['path']} failed: {result['error']}")
```

### Method 4: Parser Class (Advanced)

For integration with document processing pipelines:

```python
from src.parsers.qwen_vl_ocr_parser import QwenVLOCRParser

parser = QwenVLOCRParser(
    file_path='image.jpg',
    model='qwen-vl-ocr-latest',
    language='zh'
)

# Parse to Document objects
documents = parser.parse()
for doc in documents:
    print(f"Line {doc.metadata['line_index']}: {doc.content}")

# Or get full text
full_text = parser.parse_full_text()

# Or get detailed response
details = parser.parse_with_details()
```

## Configuration Options

### Model Selection

Available models:
- `qwen-vl-ocr-latest` (default) - Latest version, best overall performance
- `qwen-vl-max` - Maximum accuracy for complex documents
- `qwen-vl-plus` - Balanced speed and accuracy

```python
extract_text_from_image('image.jpg', model='qwen-vl-max')
```

### Language Settings

- `'zh'` - Chinese optimized (default)
- `'en'` - English optimized
- `'auto'` - Auto-detect

```python
extract_text_from_image('image.jpg', language='en')
```

### Custom Prompts

Tailor the recognition behavior:

```python
# Focus on specific content
prompt = '请识别图片中的所有数学公式'
text = extract_text_from_image('math.jpg', prompt=prompt)

# Format-specific
prompt = '请按表格格式还原图片中的内容'
text = extract_text_from_image('table.jpg', prompt=prompt)

# Quality control
prompt = '请仔细识别图片中的手写文字，确保准确性'
text = extract_text_from_image('handwriting.jpg', prompt=prompt)
```

## Error Handling

The skill handles common errors gracefully:

```python
try:
    text = extract_text_from_image('image.jpg')
except ValueError as e:
    # API Key not set
    print(f"Configuration error: {e}")
except FileNotFoundError as e:
    # Image file not found
    print(f"File error: {e}")
except RuntimeError as e:
    # API call failed
    print(f"Recognition error: {e}")
```

Or use the detailed version for programmatic handling:

```python
result = extract_text_with_details('image.jpg')
if not result['success']:
    if 'API Key' in result['error']:
        print("Please configure DASHSCOPE_API_KEY")
    elif 'not found' in result['error']:
        print("Image file does not exist")
    else:
        print(f"OCR failed: {result['error']}")
```

## Best Practices

### 1. Choose the Right Method
- Use `extract_text_from_image()` for simple text extraction
- Use `extract_text_with_details()` for debugging or logging
- Use `batch_extract_texts()` for multiple images
- Use `QwenVLOCRParser` for document processing pipelines

### 2. Optimize Prompts
Be specific about what you need:
- ❌ "识别文字" (too vague)
- ✅ "请识别图片中的所有中文标题，忽略正文内容" (specific)

### 3. Handle Failures Gracefully
Always check for success before using results:
```python
result = extract_text_with_details('image.jpg')
if result['success']:
    process_text(result['text'])
else:
    log_error(result['error'])
```

### 4. Monitor Usage
Track API consumption for cost management:
```python
result = extract_text_with_details('image.jpg')
if result['success'] and result.get('usage'):
    print(f"Tokens used: {result['usage'].get('total_tokens', 0)}")
```

## Example Workflows

### Workflow 1: Screenshot to Text

```python
from src.utils.qwen_vl_ocr import ocr

# Quick one-liner
text = ocr('screenshot.png')

# Save to file
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(text)
```

### Workflow 2: Document Digitization

```python
from src.utils.qwen_vl_ocr import batch_extract_texts
import glob

# Scan all pages
pages = sorted(glob.glob('scanned_book/page_*.jpg'))
results = batch_extract_texts(pages)

# Combine into single text
full_book = '\n'.join([r['text'] for r in results if r['success']])

with open('book.txt', 'w', encoding='utf-8') as f:
    f.write(full_book)
```

### Workflow 3: Form Processing

```python
from src.parsers.qwen_vl_ocr_parser import QwenVLOCRParser

parser = QwenVLOCRParser(
    'form.jpg',
    prompt='请识别表单中的所有字段和对应的值'
)

# Get structured data
docs = parser.parse()
form_data = {doc.content.split(':')[0]: doc.content.split(':')[1] 
             for doc in docs if ':' in doc.content}
```

## Troubleshooting

### Issue: "未找到阿里云 API Key"
**Solution:** Set the environment variable:
```bash
export DASHSCOPE_API_KEY=your_key_here
```
Or pass it directly:
```python
extract_text_from_image('image.jpg', api_key='sk-...')
```

### Issue: "OCR 识别失败：网络错误"
**Solution:** Check internet connection and retry. The API requires network access.

### Issue: Recognition quality is poor
**Solutions:**
1. Try a different model: `model='qwen-vl-max'`
2. Add a specific prompt to guide recognition
3. Ensure image quality (resolution, lighting, angle)

## Pricing Information

Qwen-VL OCR is a paid service. Check current pricing at:
https://www.aliyun.com/product/dashscope

Monitor your usage through the console to avoid unexpected charges.

## Related Resources

- Official Documentation: https://help.aliyun.com/zh/dashscope/
- API Reference: https://dashscope.console.aliyun.com/api
- Model Comparison: https://help.aliyun.com/zh/model-studio/
