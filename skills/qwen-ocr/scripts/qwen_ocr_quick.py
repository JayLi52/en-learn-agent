#!/usr/bin/env python3
"""
Qwen-VL OCR 快速识别脚本
用于从命令行快速识别图片中的文字

用法:
    python qwen_ocr_quick.py image.jpg
    python qwen_ocr_quick.py image.jpg --model qwen-vl-max
    python qwen_ocr_quick.py image1.jpg image2.png image3.jpg
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.qwen_vl_ocr import extract_text_from_image, batch_extract_texts


def main():
    parser = argparse.ArgumentParser(
        description='Qwen-VL OCR - 从图片中提取文字',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s image.jpg                    # 识别单张图片
  %(prog)s img1.jpg img2.png            # 批量识别
  %(prog)s image.jpg --model qwen-vl-max  # 使用高精度模型
  %(prog)s image.jpg --prompt "只识别标题"  # 自定义识别要求
        """
    )
    
    parser.add_argument(
        'images',
        nargs='+',
        type=str,
        help='图片文件路径（支持多个）'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='qwen-vl-ocr-latest',
        choices=['qwen-vl-ocr-latest', 'qwen-vl-max', 'qwen-vl-plus'],
        help='OCR 模型 (默认：qwen-vl-ocr-latest)'
    )
    
    parser.add_argument(
        '--api-key',
        type=str,
        default=None,
        help='阿里云 API Key (不指定则使用环境变量 DASHSCOPE_API_KEY)'
    )
    
    parser.add_argument(
        '--prompt',
        type=str,
        default='请准确完整地识别图片中的所有文字内容',
        help='识别提示词'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='显示详细信息'
    )
    
    args = parser.parse_args()
    
    # Validate files
    valid_images = []
    for img_path in args.images:
        path = Path(img_path).expanduser()
        if not path.exists():
            print(f"错误：文件不存在 - {img_path}", file=sys.stderr)
            continue
        valid_images.append(str(path))
    
    if not valid_images:
        print("错误：没有有效的图片文件", file=sys.stderr)
        sys.exit(1)
    
    try:
        if len(valid_images) == 1:
            # Single image
            if args.verbose:
                print(f"正在识别：{valid_images[0]}")
                print(f"模型：{args.model}")
                print("-" * 50)
            
            text = extract_text_from_image(
                valid_images[0],
                api_key=args.api_key,
                model=args.model,
                prompt=args.prompt
            )
            
            print(text)
            
            if args.verbose:
                print("-" * 50)
                print("识别完成")
        else:
            # Batch processing
            if args.verbose:
                print(f"批量识别 {len(valid_images)} 张图片...")
                print(f"模型：{args.model}")
                print("=" * 50)
            
            results = batch_extract_texts(
                valid_images,
                api_key=args.api_key,
                model=args.model,
                verbose=args.verbose
            )
            
            print("\n" + "=" * 50)
            print("识别结果:")
            print("=" * 50)
            
            success_count = 0
            for result in results:
                if result['success']:
                    success_count += 1
                    print(f"\n✓ {Path(result['path']).name}:")
                    print(result['text'])
                else:
                    print(f"\n✗ {Path(result['path']).name}: {result['error']}")
            
            print("\n" + "=" * 50)
            print(f"总计：{len(valid_images)} 张，成功 {success_count} 张，失败 {len(valid_images) - success_count} 张")
    
    except ValueError as e:
        print(f"\n配置错误：{e}", file=sys.stderr)
        print("\n请设置环境变量 DASHSCOPE_API_KEY", file=sys.stderr)
        print("或直接在命令中传入 --api-key 参数", file=sys.stderr)
        sys.exit(1)
    
    except FileNotFoundError as e:
        print(f"\n文件错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    except RuntimeError as e:
        print(f"\n识别失败：{e}", file=sys.stderr)
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(0)


if __name__ == '__main__':
    main()
