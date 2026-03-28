#!/usr/bin/env python3
"""
Qwen-VL OCR 批量处理脚本
用于批量识别目录中的所有图片并保存结果

用法:
    python qwen_ocr_batch.py ./input_images/ --output results.txt
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.qwen_vl_ocr import batch_extract_texts


def find_images(directory):
    """在目录中查找所有图片文件"""
    image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
    images = []
    
    dir_path = Path(directory).expanduser()
    if not dir_path.exists():
        return []
    
    for file_path in sorted(dir_path.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in image_extensions:
            images.append(str(file_path))
    
    return images


def main():
    parser = argparse.ArgumentParser(
        description='Qwen-VL OCR 批量处理 - 识别目录中的所有图片',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s ./images/                      # 识别目录下所有图片
  %(prog)s ./images/ -o results.txt       # 保存结果到文件
  %(prog)s ./images/ --format json        # 输出 JSON 格式
  %(prog)s ./images/ --model qwen-vl-max  # 使用高精度模型
        """
    )
    
    parser.add_argument(
        'directory',
        type=str,
        help='包含图片的目录'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='输出文件路径 (默认：输出到终端)'
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
        '--format',
        type=str,
        default='text',
        choices=['text', 'json', 'csv'],
        help='输出格式 (默认：text)'
    )
    
    parser.add_argument(
        '--include-filename',
        action='store_true',
        help='在输出中包含文件名'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='静默模式，不显示处理进度'
    )
    
    args = parser.parse_args()
    
    # Find images
    images = find_images(args.directory)
    
    if not images:
        print(f"错误：在 {args.directory} 中未找到图片文件", file=sys.stderr)
        print("支持的格式：.jpg, .jpeg, .png, .bmp, .tiff, .webp", file=sys.stderr)
        sys.exit(1)
    
    print(f"找到 {len(images)} 张图片")
    print(f"模型：{args.model}")
    print("-" * 50)
    
    try:
        # Process images
        results = batch_extract_texts(
            images,
            api_key=args.api_key,
            model=args.model,
            verbose=not args.quiet
        )
        
        # Generate output
        output_lines = []
        success_count = sum(1 for r in results if r['success'])
        
        if args.format == 'json':
            import json
            output_lines.append(json.dumps(results, ensure_ascii=False, indent=2))
        
        elif args.format == 'csv':
            output_lines.append("filename,success,text,error")
            for result in results:
                filename = Path(result['path']).name
                text_escaped = result['text'].replace('"', '""').replace('\n', '\\n')
                error_escaped = result['error'].replace('"', '""').replace('\n', '\\n')
                output_lines.append(f'"{filename}",{result["success"]},"{text_escaped}","{error_escaped}"')
        
        else:  # text format
            output_lines.append(f"Qwen-VL OCR 批量识别结果")
            output_lines.append(f"处理时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            output_lines.append(f"总计：{len(images)} 张，成功 {success_count} 张，失败 {len(images) - success_count} 张")
            output_lines.append("=" * 50)
            
            for result in results:
                if result['success']:
                    if args.include_filename:
                        output_lines.append(f"\n【{Path(result['path']).name}】")
                    output_lines.append(result['text'])
                    output_lines.append("-" * 30)
        
        output_text = '\n'.join(output_lines)
        
        # Save or display
        if args.output:
            output_path = Path(args.output).expanduser()
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output_text)
            print(f"\n结果已保存到：{output_path}")
        else:
            print("\n" + "=" * 50)
            print(output_text)
        
        # Summary
        print("\n" + "=" * 50)
        print(f"处理完成：{success_count}/{len(images)} 成功")
        
        if success_count < len(images):
            failed = [r for r in results if not r['success']]
            print(f"\n失败的 {len(failed)} 个文件:")
            for result in failed:
                print(f"  - {Path(result['path']).name}: {result['error']}")
    
    except ValueError as e:
        print(f"\n配置错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    except Exception as e:
        print(f"\n处理失败：{e}", file=sys.stderr)
        sys.exit(1)
    
    except KeyboardInterrupt:
        print("\n\n用户中断")
        sys.exit(0)


if __name__ == '__main__':
    main()
