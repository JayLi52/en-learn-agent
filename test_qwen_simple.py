#!/usr/bin/env python3
"""Qwen-VL OCR 快速测试 - 简洁版"""
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# 检查 API Key
api_key = os.getenv('DASHSCOPE_API_KEY')
if not api_key:
    print("="*60)
    print("⚠️  未设置 DASHSCOPE_API_KEY 环境变量")
    print("="*60)
    print("\n请执行以下命令:")
    print("export DASHSCOPE_API_KEY=your-api-key-here")
    print("\n获取 API Key: https://dashscope.console.aliyun.com/apiKey")
    sys.exit(1)

if len(sys.argv) < 2:
    print("="*60)
    print("Qwen-VL OCR 快速测试")
    print("="*60)
    print("\n用法：python test_qwen_simple.py <图片路径>")
    print("\n示例：python test_qwen_simple.py zuowen.jpg")
    print("\n特性:")
    print("  ✓ 使用 qwen-vl-ocr-latest 模型")
    print("  ✓ 简洁的工具函数接口")
    print("  ✓ 云端 GPU 加速")
    print("="*60)
    sys.exit(1)

image_path = Path(sys.argv[1]).expanduser()

if not image_path.exists():
    print(f"✗ 图片不存在：{image_path}")
    sys.exit(1)

print("="*60)
print("正在识别:", image_path.name)
print("="*60)

try:
    from src.utils import extract_text_from_image
    
    # 直接调用函数，就是这么简单!
    text = extract_text_from_image(image_path)
    
    print("\n✓ 识别成功!\n")
    print("-"*60)
    print(text)
    print("-"*60)
    print("\n✓ 完成!")
    
except Exception as e:
    print(f"\n✗ 识别失败：{e}")
    sys.exit(1)
