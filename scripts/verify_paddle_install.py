"""验证 PaddleOCR 安装是否正确"""
import sys


def check_paddle_installation():
    """检查 PaddlePaddle 安装"""
    print("="*60)
    print("PaddleOCR 安装验证")
    print("="*60)
    
    # 1. 检查 PaddlePaddle
    print("\n1. 检查 PaddlePaddle...")
    try:
        import paddle
        print(f"   ✓ PaddlePaddle 版本：{paddle.__version__}")
        
        # 检查 GPU 支持
        try:
            is_gpu_available = paddle.is_compiled_with_cuda() or hasattr(paddle.device, 'get_device')
            device = paddle.device.get_device()
            print(f"   ✓ 可用设备：{device}")
            
            if 'gpu' in device.lower():
                print(f"   ✓ GPU 加速已启用")
            else:
                print(f"   ℹ 使用 CPU 模式 (Mac 会自动调用 Metal)")
                
        except Exception as e:
            print(f"   ⚠ 设备检测：{e}")
            
    except ImportError:
        print("   ✗ PaddlePaddle 未安装")
        return False
    
    # 2. 检查 PaddleOCR
    print("\n2. 检查 PaddleOCR...")
    try:
        from paddleocr import PaddleOCR
        print(f"   ✓ PaddleOCR 已安装")
        
        # 尝试初始化
        print("\n3. 测试 OCR 初始化...")
        ocr = PaddleOCR(
            use_textline_orientation=True,
            lang='ch'
        )
        print(f"   ✓ OCR 引擎初始化成功")
        
    except ImportError:
        print("   ✗ PaddleOCR 未安装")
        return False
    except Exception as e:
        print(f"   ✗ 初始化失败：{e}")
        return False
    
    # 3. 系统信息
    print("\n4. 系统信息:")
    import platform
    print(f"   操作系统：{platform.system()} {platform.release()}")
    print(f"   Python 版本：{sys.version}")
    print(f"   芯片架构：{platform.machine()}")
    
    print("\n" + "="*60)
    print("✓ PaddleOCR 安装验证通过!")
    print("="*60)
    print("\n可以开始使用 OCR 功能了!")
    print("运行：python quick_ocr.py <图片路径>")
    print("="*60)
    
    return True


if __name__ == '__main__':
    success = check_paddle_installation()
    sys.exit(0 if success else 1)
