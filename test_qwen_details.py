#!/usr/bin/env python3
"""测试 Qwen-VL OCR 返回的详细信息"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from src.utils import extract_text_with_details

# 测试图片
image_path = Path('zuowen.jpg')

print("="*60)
print("测试 Qwen-VL OCR 返回的详细信息")
print("="*60)

result = extract_text_with_details(image_path)

print("\n📊 返回结果:")
print("-"*60)
for key, value in result.items():
    if key == 'text':
        print(f"{key}: (文字内容，共{len(value)}字符)")
    elif key == 'usage':
        print(f"{key}:")
        if value:
            for k, v in value.items():
                print(f"  - {k}: {v}")
        else:
            print(f"  - {value}")
    else:
        print(f"{key}: {value}")

print("-"*60)

# 显示实际文字
if result['success']:
    print("\n📝 识别的文字内容:")
    print("-"*60)
    print(result['text'])
    print("-"*60)
