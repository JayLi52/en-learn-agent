"""PaddleOCR 图片文字识别解析器
纯本地离线运行，自动调用 Mac GPU(Metal) 加速
适配 M1/M2/M3/M4/Intel 芯片
"""
from pathlib import Path
from typing import List, Optional, Union
import os
from .base import BaseParser, Document


class PaddleOCRParser(BaseParser):
    """PaddleOCR 解析器 - 支持中文/英文/混合排版识别"""
    
    def __init__(
        self,
        file_path: Union[str, Path],
        det_model_dir: Optional[str] = None,
        rec_model_dir: Optional[str] = None,
        cls_model_dir: Optional[str] = None,
        use_angle_cls: bool = True,
        lang: str = 'ch'
    ):
        """
        Args:
            file_path: 图片文件路径
            det_model_dir: 文本检测模型路径 (可选，不传则用默认模型)
            rec_model_dir: 文本识别模型路径 (可选，不传则用默认模型)
            cls_model_dir: 方向分类模型路径 (可选，不传则用默认模型)
            use_angle_cls: 是否使用方向分类器 (倾斜文字修正)
            lang: 识别语言，'ch'=中英文混合，'en'=英文
        """
        super().__init__(file_path)
        self.det_model_dir = det_model_dir
        self.rec_model_dir = rec_model_dir
        self.cls_model_dir = cls_model_dir
        self.use_angle_cls = use_angle_cls
        self.lang = lang
        self._ocr = None
    
    def _init_ocr(self):
        """延迟初始化 PaddleOCR(首次调用时加载)"""
        if self._ocr is None:
            from paddleocr import PaddleOCR
            
            # 构建 OCR 实例 (PaddleOCR 3.x API)
            # 优化配置：减少内存占用，提升速度
            ocr_config = {
                'use_textline_orientation': self.use_angle_cls,  # 使用新的方向分类参数
                'lang': self.lang,
                'text_det_thresh': 0.3,
                'text_det_box_thresh': 0.5,
                'text_rec_score_thresh': 0.5,  # 提高阈值，减少无效结果
            }
            
            # 如果指定了本地模型路径，使用自定义模型
            if self.det_model_dir:
                ocr_config['text_detection_model_dir'] = self.det_model_dir
            if self.rec_model_dir:
                ocr_config['text_recognition_model_dir'] = self.rec_model_dir
            if self.cls_model_dir:
                ocr_config['textline_orientation_model_dir'] = self.cls_model_dir
            
            self._ocr = PaddleOCR(**ocr_config)
    
    def parse(self) -> List[Document]:
        """执行 OCR 识别
        
        Returns:
            Document 列表，每个 Document 包含识别的文字和置信度
        """
        self.validate_file()
        self._init_ocr()
        
        # 执行 OCR 识别 (PaddleOCR 3.x API)
        result = self._ocr.predict(str(self.file_path))
        
        # 解析结果 (PaddleOCR 3.x 返回字典列表)
        documents = []
        if result and len(result) > 0:
            # 获取第一个 (也是唯一一个) 结果字典
            ocr_result = result[0]
            
            # 提取文字、置信度和位置
            rec_texts = ocr_result.get('rec_texts', [])
            rec_scores = ocr_result.get('rec_scores', [])
            
            for line_idx, text in enumerate(rec_texts):
                confidence = rec_scores[line_idx] if line_idx < len(rec_scores) else 0.0
                
                doc = Document(
                    content=text,
                    source=str(self.file_path),
                    page=None,  # 图片无页码概念
                    metadata={
                        'confidence': confidence,
                        'line_index': line_idx,
                        'type': 'ocr_text'
                    }
                )
                documents.append(doc)
        
        return documents
    
    def parse_full_text(self) -> str:
        """识别并返回完整文字内容 (拼接所有识别结果)
        
        Returns:
            完整的识别文字字符串
        """
        docs = self.parse()
        return '\n'.join([doc.content for doc in docs])
    
    def parse_with_position(self) -> List[dict]:
        """识别并返回带位置信息的文字
        
        Returns:
            包含文字、置信度、坐标位置的字典列表
        """
        self.validate_file()
        self._init_ocr()
        
        # 执行 OCR 识别 (PaddleOCR 3.x API)
        result = self._ocr.predict(str(self.file_path))
        
        output = []
        if result and len(result) > 0:
            ocr_result = result[0]
            
            rec_texts = ocr_result.get('rec_texts', [])
            rec_scores = ocr_result.get('rec_scores', [])
            rec_polys = ocr_result.get('rec_polys', [])
            
            for idx, text in enumerate(rec_texts):
                confidence = rec_scores[idx] if idx < len(rec_scores) else 0.0
                position = rec_polys[idx] if idx < len(rec_polys) else None
                
                if position is not None and len(position) >= 4:
                    output.append({
                        'text': text,
                        'confidence': confidence,
                        'position': position.tolist() if hasattr(position, 'tolist') else position,
                        'box': {
                            'top_left': position[0].tolist() if hasattr(position[0], 'tolist') else position[0].tolist(),
                            'top_right': position[1].tolist() if hasattr(position[1], 'tolist') else position[1].tolist(),
                            'bottom_right': position[2].tolist() if hasattr(position[2], 'tolist') else position[2].tolist(),
                            'bottom_left': position[3].tolist() if hasattr(position[3], 'tolist') else position[3].tolist()
                        }
                    })
        
        return output


async def create_paddle_ocr_parser(
    image_path: Union[str, Path],
    models_base_dir: Optional[str] = None,
    lang: str = 'ch'
) -> PaddleOCRParser:
    """工厂函数：创建 PaddleOCR 解析器实例
    
    Args:
        image_path: 图片路径
        models_base_dir: 模型基础目录 (可选)
                        如果提供，会自动查找以下子目录:
                        - ch_PP-OCRv5_det_infer
                        - ch_PP-OCRv5_rec_infer  
                        - ch_ppocr_mobile_v2.0_cls_infer
        lang: 识别语言
    
    Returns:
        PaddleOCRParser 实例
    """
    if models_base_dir:
        base = Path(models_base_dir).expanduser()
        return PaddleOCRParser(
            file_path=image_path,
            det_model_dir=str(base / 'ch_PP-OCRv5_det_infer'),
            rec_model_dir=str(base / 'ch_PP-OCRv5_rec_infer'),
            cls_model_dir=str(base / 'ch_ppocr_mobile_v2.0_cls_infer'),
            lang=lang
        )
    else:
        # 使用 PaddleOCR 默认模型 (首次会自动下载)
        return PaddleOCRParser(file_path=image_path, lang=lang)
