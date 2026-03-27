#!/usr/bin/env python3
"""PaddleOCR 快速启动脚本
一键启动 OCR 识别，自动检测和安装依赖
"""
import sys
import subprocess
from pathlib import Path


def check_and_install_paddle():
    """检查并安装 PaddleOCR"""
    try:
        import paddle
        # 延迟导入 paddleocr，避免与其他库冲突
        print("✓ PaddlePaddle 已安装")
        return True
    except ImportError:
        print("⚠ 未检测到 PaddlePaddle，正在安装...")
        
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "paddlepaddle",
            "-i",
            "https://www.paddlepaddle.org.cn/packages/stable/cpu/"
        ])
        
        print("✓ PaddlePaddle 安装完成!")
        return True


def main():
    """主函数"""
    # 检查依赖
    check_and_install_paddle()
    
    # 检查图片参数
    if len(sys.argv) < 2:
        print("="*60)
        print("PaddleOCR 快速识别工具")
        print("="*60)
        print("\n用法：python quick_ocr.py <图片路径> [模型目录]")
        print("\n示例:")
        print("  python quick_ocr.py test.jpg")
        print("  python quick_ocr.py test.jpg ~/Desktop/paddle_ocr/models")
        print("\n支持格式：JPG, PNG, BMP, WEBP")
        print("特性：纯本地离线 | 自动 GPU 加速 | 中英文混合识别")
        print("="*60)
        sys.exit(1)
    
    image_path = Path(sys.argv[1]).expanduser()
    models_dir = Path(sys.argv[2]).expanduser() if len(sys.argv) > 2 else None
    
    if not image_path.exists():
        print(f"✗ 图片不存在：{image_path}")
        sys.exit(1)
    
    # 导入解析器
    from src.parsers import PaddleOCRParser
    
    # 创建解析器
    if models_dir and models_dir.exists():
        print(f"使用本地模型：{models_dir}")
        parser = PaddleOCRParser(
            file_path=image_path,
            det_model_dir=str(models_dir / 'ch_PP-OCRv5_det_infer'),
            rec_model_dir=str(models_dir / 'ch_PP-OCRv5_rec_infer'),
            cls_model_dir=str(models_dir / 'ch_ppocr_mobile_v2.0_cls_infer'),
            use_angle_cls=True,
            lang='ch'
        )
    else:
        print("使用默认模型 (首次运行会自动下载)")
        parser = PaddleOCRParser(image_path, use_angle_cls=True, lang='ch')
    
    # 执行识别
    print(f"\n正在识别：{image_path.name}...")
    print("-"*60)
    
    documents = parser.parse()
    
    # 输出结果
    if documents:
        print(f"\n✓ 识别成功！共 {len(documents)} 行文字:\n")
        for i, doc in enumerate(documents, 1):
            confidence = doc.metadata.get('confidence', 0)
            print(f"{i:2d}. {doc.content} (置信度：{confidence:.2f})")
        
        print("\n" + "="*60)
        print("完整文本:")
        print("="*60)
        print(parser.parse_full_text())
    else:
        print("✗ 未识别到任何文字")
    
    print("\n✓ 完成!")


if __name__ == '__main__':
    main()
