#!/usr/bin/env python3
"""PaddleOCR 高性能识别脚本 - 使用 PP-OCRv5 最优模型"""
import sys
import os
from pathlib import Path

# 设置环境变量，优化性能
os.environ['FLAGS_cinn'] = '0'  # 禁用 CINN 编译器，减少内存
os.environ['FLAGS_use_mkldnn'] = '1'  # 启用 MKLDNN 加速

if len(sys.argv) < 2:
    print("="*60)
    print("PaddleOCR 高性能 OCR 识别")
    print("="*60)
    print("\n用法：python best_ocr.py <图片路径>")
    print("\n示例：python best_ocr.py zuowen.jpg")
    print("\n特性:")
    print("- 使用 PP-OCRv5 server 级模型 (效果最好)")
    print("- 自动方向修正")
    print("- 高置信度过滤")
    print("="*60)
    sys.exit(1)

image_path = Path(sys.argv[1]).expanduser()

if not image_path.exists():
    print(f"✗ 图片不存在：{image_path}")
    sys.exit(1)

print("="*60)
print("正在加载 PaddleOCR PP-OCRv5 模型...")
print("(首次加载较慢，后续会快很多)")
print("="*60)

try:
    from src.parsers import PaddleOCRParser
    
    print("\n创建解析器...")
    parser = PaddleOCRParser(
        file_path=image_path,
        use_angle_cls=True,  # 开启方向修正
        lang='ch'
    )
    
    print(f"\n正在识别：{image_path.name}...")
    print("-"*60)
    
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
