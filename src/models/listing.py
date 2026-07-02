"""
产品B v0.3 - 上架包生成模型
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class TitleGeneration:
    """标题生成记录"""
    id: str
    product_id: str
    titles: List[str]  # 20个标题
    generation_method: str  # "template" or "llm"
    merchant_profile_id: Optional[str] = None
    keyword_library_id: Optional[str] = None
    visual_style_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "titles": self.titles,
            "generation_method": self.generation_method,
            "merchant_profile_id": self.merchant_profile_id,
            "keyword_library_id": self.keyword_library_id,
            "visual_style_id": self.visual_style_id,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class KeywordGeneration:
    """关键词生成记录"""
    id: str
    product_id: str
    core_keywords: List[str]  # 核心关键词
    long_tail_keywords: List[str]  # 长尾关键词
    audience_keywords: List[str]  # 人群关键词
    scenario_keywords: List[str]  # 场景关键词
    selling_point_keywords: List[str]  # 卖点关键词
    ad_keywords: List[str]  # 投放关键词候选
    negative_keywords: List[str]  # 否词候选
    generation_method: str  # "template" or "llm"
    keyword_library_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "core_keywords": self.core_keywords,
            "long_tail_keywords": self.long_tail_keywords,
            "audience_keywords": self.audience_keywords,
            "scenario_keywords": self.scenario_keywords,
            "selling_point_keywords": self.selling_point_keywords,
            "ad_keywords": self.ad_keywords,
            "negative_keywords": self.negative_keywords,
            "generation_method": self.generation_method,
            "keyword_library_id": self.keyword_library_id,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ImagePrompt:
    """单张主图提示词"""
    image_type: str  # 图片类型：白底主图、模特上身图、高级质感图等
    purpose: str  # 图片用途
    structure: str  # 画面结构
    focus: str  # 商品展示重点
    ai_prompt_cn: str  # AI作图中文提示词
    ai_prompt_en: str  # 适合复制到即梦/万相的提示词
    notes: str  # 注意事项


@dataclass
class ImagePromptGeneration:
    """主图九宫格提示词生成记录"""
    id: str
    product_id: str
    prompts: List[ImagePrompt]  # 9张主图提示词
    generation_method: str  # "template" or "llm"
    visual_style_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "prompts": [
                {
                    "image_type": p.image_type,
                    "purpose": p.purpose,
                    "structure": p.structure,
                    "focus": p.focus,
                    "ai_prompt_cn": p.ai_prompt_cn,
                    "ai_prompt_en": p.ai_prompt_en,
                    "notes": p.notes
                }
                for p in self.prompts
            ],
            "generation_method": self.generation_method,
            "visual_style_id": self.visual_style_id,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ListingPackage:
    """上架包"""
    id: str
    product_id: str
    product_info: Dict[str, Any]  # 产品基础信息
    titles: List[str]  # 20个标题
    keywords: Dict[str, List[str]]  # 关键词包
    image_prompts: List[Dict[str, Any]]  # 主图九宫格提示词
    merchant_profile: Optional[Dict[str, Any]] = None  # 使用的商家档案
    visual_style: Optional[Dict[str, Any]] = None  # 使用的视觉风格
    pending_review: List[str] = field(default_factory=list)  # 待人工确认事项
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_info": self.product_info,
            "titles": self.titles,
            "keywords": self.keywords,
            "image_prompts": self.image_prompts,
            "merchant_profile": self.merchant_profile,
            "visual_style": self.visual_style,
            "pending_review": self.pending_review,
            "created_at": self.created_at.isoformat()
        }
