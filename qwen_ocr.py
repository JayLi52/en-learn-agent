#!/usr/bin/env python3
"""阿里云 Qwen-VL OCR 快速识别脚本
使用 qwen-vl-ocr-latest 模型，识别效果业界顶尖
"""
import sys
import os
from pathlib import Path

# 检查 API Key
api_key = os.getenv('DASHSCOPE_API_KEY')
if not api_key:
    print("="*60)
    print("⚠️  未找到阿里云 API Key")
    print("="*60)
    print("\n请设置环境变量 DASHSCOPE_API_KEY:")
    print("1. 获取 API Key: https://dashscope.console.aliyun.com/apiKey")
    print("2. 在终端执行:")
    print("   export DASHSCOPE_API_KEY=your-api-key-here")
    print("3. 或者添加到 .env 文件")
    print("="*60)
    sys.exit(1)

if len(sys.argv) < 2:
    print("="*60)
    print("阿里云 Qwen-VL OCR 识别工具")
    print("="*60)
    print("\n用法：python qwen_ocr.py <图片路径>")
    print("\n示例:")
    print("  python qwen_ocr.py zuowen.jpg")
    print("  python qwen_ocr.py document.png")
    print("\n特性:")
    print("  ✓ 使用 qwen-vl-ocr-latest 模型 (效果顶尖)")
    print("  ✓ 支持复杂文档、表格、公式、手写体")
    print("  ✓ 自动语言检测")
    print("  ✓ 云端 GPU 加速，速度快")
    print("="*60)
    sys.exit(1)

image_path = Path(sys.argv[1]).expanduser()

if not image_path.exists():
    print(f"✗ 图片不存在：{image_path}")
    sys.exit(1)

print("="*60)
print("正在调用阿里云 Qwen-VL OCR...")
print("="*60)

try:
    from src.parsers import QwenVLOCRParser
    
    # 创建解析器
    parser = QwenVLOCRParser(
        file_path=image_path,
        model='qwen-vl-ocr-latest',
        language='auto'  # 自动检测语言
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
        print("✓ 完成!")
        print("="*60)
    else:
        print("✗ 未识别到任何文字")
        
except Exception as e:
    print(f"\n✗ 识别失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
