"""测试阿里云 Qwen-VL OCR 识别效果"""
import os
from pathlib import Path
from src.parsers import QwenVLOCRParser
from dotenv import load_dotenv

# 加载 .env 文件中的环境变量
load_dotenv()
# 检查 API Key
api_key = os.getenv('DASHSCOPE_API_KEY')
if not api_key:
    print("⚠️  未设置 DASHSCOPE_API_KEY 环境变量")
    print("\n请执行以下命令:")
    print("export DASHSCOPE_API_KEY=your-api-key-here")
    print("\n获取 API Key: https://dashscope.console.aliyun.com/apiKey")
    exit(1)

print("="*60)
print("阿里云 Qwen-VL OCR 测试 - qwen-vl-ocr-latest")
print("="*60)

image_path = Path('zuowen.jpg')

if not image_path.exists():
    print(f"✗ 图片不存在：{image_path}")
    exit(1)

try:
    # 创建解析器
    parser = QwenVLOCRParser(
        file_path=image_path,
        model='qwen-vl-ocr-latest',
        language='auto'
    )
    
    print(f"\n正在识别：{image_path.name}...")
    print("-"*60)
    
    # 执行识别
    documents = parser.parse()
    
    if documents:
        print(f"\n✓ 识别成功！共 {len(documents)} 行文字:\n")
        for i, doc in enumerate(documents, 1):
            confidence = doc.metadata.get('confidence', 0)
            print(f"{i:2d}. {doc.content} (置信度：{confidence:.2f})")
        
        print("\n" + "="*60)
        print("完整文本:")
        print("="*60)
        full_text = parser.parse_full_text()
        print(full_text)
        
        print("\n" + "="*60)
        print("✓ 测试完成!")
        print("="*60)
    else:
        print("✗ 未识别到任何文字")
        
except Exception as e:
    print(f"\n✗ 识别失败：{e}")
    import traceback
    traceback.print_exc()
