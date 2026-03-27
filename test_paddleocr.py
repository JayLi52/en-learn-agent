"""PaddleOCR 快速测试脚本
创建测试图片并执行 OCR 识别
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from src.parsers import PaddleOCRParser


def create_test_image():
    """创建一张包含中英文的测试图片"""
    # 创建白色背景图片
    width, height = 800, 600
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # 绘制文字
    text_lines = [
        "Hello World!",
        "你好，世界！",
        "PaddleOCR 测试",
        "这是一张测试图片",
        "Mac M1/M2/M3 自动加速",
        "纯本地离线运行",
    ]
    
    y_position = 50
    for line in text_lines:
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 40)
        except:
            # 如果找不到，使用默认字体
            font = ImageFont.load_default()
        
        # 计算文字位置使其居中
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x_position = (width - text_width) // 2
        
        # 绘制文字
        draw.text((x_position, y_position), line, fill='black', font=font)
        y_position += 80
    
    # 保存图片
    test_img_path = Path(__file__).parent / 'test_ocr_sample.jpg'
    image.save(test_img_path)
    print(f"✓ 测试图片已保存：{test_img_path}")
    return test_img_path


def test_basic_ocr(image_path):
    """测试基础 OCR 功能"""
    print("\n" + "="*60)
    print("测试 1: 基础 OCR 识别")
    print("="*60)
    
    parser = PaddleOCRParser(image_path)
    docs = parser.parse()
    
    if docs:
        print(f"\n✓ 识别成功！共 {len(docs)} 行文字:\n")
        for i, doc in enumerate(docs, 1):
            confidence = doc.metadata.get('confidence', 0)
            print(f"{i:2d}. {doc.content} (置信度：{confidence:.2f})")
        
        print("\n" + "="*60)
        print("完整文本:")
        print("="*60)
        print(parser.parse_full_text())
    else:
        print("✗ 未识别到任何文字")


def test_with_position(image_path):
    """测试带位置信息的 OCR"""
    print("\n" + "="*60)
    print("测试 2: 获取文字位置信息")
    print("="*60)
    
    parser = PaddleOCRParser(image_path)
    results = parser.parse_with_position()
    
    print(f"\n识别到 {len(results)} 个文字块:\n")
    for i, item in enumerate(results, 1):
        print(f"{i}. 文字：{item['text']}")
        print(f"   置信度：{item['confidence']:.2f}")
        print(f"   左上角坐标：{item['box']['top_left']}")
        print()


def main():
    """主函数"""
    print("="*60)
    print("PaddleOCR 快速测试")
    print("="*60)
    
    # 创建测试图片
    test_img = create_test_image()
    
    # 测试基础 OCR
    test_basic_ocr(test_img)
    
    # 测试位置信息
    test_with_position(test_img)
    
    print("\n" + "="*60)
    print("✓ 所有测试完成!")
    print("="*60)


if __name__ == '__main__':
    main()
