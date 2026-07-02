"""
产品B v0.2 - 商家数据喂养模型
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class Platform(str, Enum):
    """平台类型"""
    TAOBAO = "淘宝"
    TMALL = "天猫"
    DOUYIN = "抖音"
    PINDUODUO = "拼多多"
    OTHER = "其他"


class PriceRange(str, Enum):
    """价格段"""
    LOW = "低价（0-50元）"
    MEDIUM_LOW = "中低价（50-100元）"
    MEDIUM = "中价（100-300元）"
    MEDIUM_HIGH = "中高价（300-500元）"
    HIGH = "高价（500-1000元）"
    LUXURY = "奢华（1000元以上）"


@dataclass
class MerchantProfile:
    """商家档案"""
    id: str
    merchant_name: str              # 商家名称
    platforms: List[Platform]       # 店铺平台
    main_category: str              # 主营类目
    price_range: PriceRange         # 价格段
    target_audience: str            # 目标人群
    positioning: str                # 店铺定位
    visual_style: str               # 视觉风格
    operation_goal: str             # 运营目标

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "merchant_name": self.merchant_name,
            "platforms": [p.value for p in self.platforms],
            "main_category": self.main_category,
            "price_range": self.price_range.value,
            "target_audience": self.target_audience,
            "positioning": self.positioning,
            "visual_style": self.visual_style,
            "operation_goal": self.operation_goal,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ProductKnowledge:
    """产品知识库"""
    id: str
    product_name: str               # 产品名称
    category: str                   # 类目
    sku: Optional[str] = None       # SKU
    price: float = 0.0              # 价格
    selling_points: List[str] = field(default_factory=list)  # 卖点
    material: Optional[str] = None  # 材质
    target_audience: Optional[str] = None  # 适用人群
    style: Optional[str] = None     # 风格
    notes: Optional[str] = None     # 备注

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "product_name": self.product_name,
            "category": self.category,
            "sku": self.sku,
            "price": self.price,
            "selling_points": self.selling_points,
            "material": self.material,
            "target_audience": self.target_audience,
            "style": self.style,
            "notes": self.notes,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class CompetitorKnowledge:
    """竞品知识库"""
    id: str
    competitor_url: str             # 竞品链接
    competitor_title: str           # 竞品标题
    price: float = 0.0              # 价格
    selling_points: List[str] = field(default_factory=list)  # 卖点
    main_image_style: Optional[str] = None  # 主图风格
    detail_page_structure: Optional[str] = None  # 详情页结构
    learnable_points: List[str] = field(default_factory=list)  # 可学习点
    differentiation_opportunity: Optional[str] = None  # 差异化机会

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "competitor_url": self.competitor_url,
            "competitor_title": self.competitor_title,
            "price": self.price,
            "selling_points": self.selling_points,
            "main_image_style": self.main_image_style,
            "detail_page_structure": self.detail_page_structure,
            "learnable_points": self.learnable_points,
            "differentiation_opportunity": self.differentiation_opportunity,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class KeywordLibrary:
    """关键词库"""
    id: str
    core_keywords: List[str] = field(default_factory=list)       # 核心词
    long_tail_keywords: List[str] = field(default_factory=list)  # 长尾词
    audience_keywords: List[str] = field(default_factory=list)   # 人群词
    scenario_keywords: List[str] = field(default_factory=list)   # 场景词
    selling_point_keywords: List[str] = field(default_factory=list)  # 卖点词
    ad_keywords: List[str] = field(default_factory=list)         # 投放词
    negative_keywords: List[str] = field(default_factory=list)   # 否词候选

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "core_keywords": self.core_keywords,
            "long_tail_keywords": self.long_tail_keywords,
            "audience_keywords": self.audience_keywords,
            "scenario_keywords": self.scenario_keywords,
            "selling_point_keywords": self.selling_point_keywords,
            "ad_keywords": self.ad_keywords,
            "negative_keywords": self.negative_keywords,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class VisualStyleLibrary:
    """视觉风格库"""
    id: str
    main_image_style: str           # 主图风格
    detail_page_style: str          # 详情页风格
    model_style: Optional[str] = None   # 模特风格
    scenario_style: Optional[str] = None  # 场景风格
    color_tone: Optional[str] = None     # 色调
    composition_method: Optional[str] = None  # 构图方式
    ai_image_prompt_template: Optional[str] = None  # AI作图提示词模板

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "main_image_style": self.main_image_style,
            "detail_page_style": self.detail_page_style,
            "model_style": self.model_style,
            "scenario_style": self.scenario_style,
            "color_tone": self.color_tone,
            "composition_method": self.composition_method,
            "ai_image_prompt_template": self.ai_image_prompt_template,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ReviewRecord:
    """复盘记录库"""
    id: str
    action_type: str                # 动作类型
    action_content: str             # 执行内容
    action_result: str              # 执行结果
    exposure: Optional[int] = None  # 曝光
    click_rate: Optional[float] = None   # 点击率
    conversion_rate: Optional[float] = None  # 转化率
    roi: Optional[float] = None     # ROI
    problem_judgment: Optional[str] = None  # 问题判断
    next_step_suggestion: Optional[str] = None  # 下一步建议

    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "action_type": self.action_type,
            "action_content": self.action_content,
            "action_result": self.action_result,
            "exposure": self.exposure,
            "click_rate": self.click_rate,
            "conversion_rate": self.conversion_rate,
            "roi": self.roi,
            "problem_judgment": self.problem_judgment,
            "next_step_suggestion": self.next_step_suggestion,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
