"""PaddleOCR 模型管理工具
用于下载和管理本地离线模型
"""
import os
import tarfile
from pathlib import Path
from typing import Optional
import urllib.request


class PaddleOCRModelManager:
    """PP-OCRv5 模型管理器"""
    
    # PP-OCRv5 模型下载链接
    MODELS = {
        'det': {
            'url': 'https://paddle-model-ecology.bj.bcebos.com/paddlex/weights/det/ch_PP-OCRv5_det_infer.tar',
            'name': 'ch_PP-OCRv5_det_infer',
            'description': '文本检测模型 (15MB)'
        },
        'rec': {
            'url': 'https://paddle-model-ecology.bj.bcebos.com/paddlex/weights/rec/ch_PP-OCRv5_rec_infer.tar',
            'name': 'ch_PP-OCRv5_rec_infer',
            'description': '文本识别模型 (10MB)'
        },
        'cls': {
            'url': 'https://paddle-model-ecology.bj.bcebos.com/paddlex/weights/cls/ch_ppocr_mobile_v2.0_cls_infer.tar',
            'name': 'ch_ppocr_mobile_v2.0_cls_infer',
            'description': '方向分类模型 (2MB)'
        }
    }
    
    def __init__(self, base_dir: Optional[str] = None):
        """
        Args:
            base_dir: 模型存储基础目录
                     默认：~/paddleocr_models
        """
        if base_dir:
            self.base_dir = Path(base_dir).expanduser()
        else:
            self.base_dir = Path.home() / 'paddleocr_models'
        
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def download_model(self, model_type: str, force: bool = False) -> Path:
        """下载单个模型
        
        Args:
            model_type: 模型类型 ('det' | 'rec' | 'cls')
            force: 是否强制重新下载
        
        Returns:
            模型目录路径
        """
        if model_type not in self.MODELS:
            raise ValueError(f"不支持的模型类型：{model_type}")
        
        model_info = self.MODELS[model_type]
        model_dir = self.base_dir / model_info['name']
        
        # 检查是否已存在
        if model_dir.exists() and not force:
            print(f"✓ 模型已存在：{model_dir}")
            return model_dir
        
        # 下载模型
        print(f"正在下载 {model_info['description']}...")
        tar_path = self.base_dir / f"{model_info['name']}.tar"
        
        try:
            # 下载文件
            urllib.request.urlretrieve(model_info['url'], tar_path)
            
            # 解压
            print(f"解压模型...")
            with tarfile.open(tar_path, 'r') as tar:
                tar.extractall(path=self.base_dir)
            
            # 清理压缩包
            tar_path.unlink()
            
            print(f"✓ 模型下载完成：{model_dir}")
            return model_dir
            
        except Exception as e:
            print(f"✗ 下载失败：{e}")
            if tar_path.exists():
                tar_path.unlink()
            raise
    
    def download_all_models(self, force: bool = False) -> dict:
        """下载所有模型
        
        Args:
            force: 是否强制重新下载
        
        Returns:
            模型类型到路径的映射字典
        """
        model_paths = {}
        
        print("="*50)
        print("开始下载 PaddleOCR PP-OCRv5 模型包")
        print("="*50)
        
        for model_type in self.MODELS.keys():
            path = self.download_model(model_type, force)
            model_paths[model_type] = path
        
        print("="*50)
        print(f"✓ 所有模型下载完成！")
        print(f"模型存储位置：{self.base_dir}")
        print("="*50)
        
        return model_paths
    
    def check_models_exist(self) -> dict:
        """检查模型是否存在
        
        Returns:
            模型存在状态字典
        """
        status = {}
        for model_type, info in self.MODELS.items():
            model_path = self.base_dir / info['name']
            status[model_type] = {
                'exists': model_path.exists(),
                'path': str(model_path)
            }
        return status
    
    def get_models_config(self) -> Optional[dict]:
        """获取模型配置 (如果所有模型都存在)
        
        Returns:
            模型路径配置字典，如果缺少模型则返回 None
        """
        status = self.check_models_exist()
        
        if not all(s['exists'] for s in status.values()):
            missing = [k for k, v in status.items() if not v['exists']]
            print(f"缺少模型：{', '.join(missing)}")
            return None
        
        return {
            'det_model_dir': status['det']['path'],
            'rec_model_dir': status['rec']['path'],
            'cls_model_dir': status['cls']['path']
        }


def quick_setup_models(output_dir: Optional[str] = None) -> dict:
    """快速设置模型 (一键下载所有模型)
    
    Args:
        output_dir: 输出目录 (可选)
    
    Returns:
        模型配置字典
    """
    manager = PaddleOCRModelManager(output_dir)
    return manager.download_all_models()


if __name__ == '__main__':
    # 示例：下载所有模型
    import sys
    
    if len(sys.argv) > 1:
        # 指定下载目录
        models_dir = sys.argv[1]
        config = quick_setup_models(models_dir)
    else:
        # 使用默认目录
        config = quick_setup_models()
    
    print("\n模型配置:")
    for key, value in config.items():
        print(f"  {key}: {value}")
