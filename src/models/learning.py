"""
产品B - 学习中心数据模型
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class LearningTarget(str, Enum):
    """学习目标"""
    COMPETITOR = "competitor"        # 竞品
    PLATFORM_RULE = "platform_rule"  # 平台规则
    PRODUCT_PAGE = "product_page"    # 商品页
    ARTICLE = "article"              # 文章
    OTHER = "other"                  # 其他


class DataType(str, Enum):
    """数据类型"""
    PRODUCT = "product"              # 产品表
    AD_DATA = "ad_data"              # 投放数据
    SALES_DATA = "sales_data"        # 销售数据
    COMPETITOR_DATA = "competitor_data"  # 竞品数据


class LinkLearningStatus(str, Enum):
    """链接学习状态"""
    PENDING = "pending"              # 待处理
    SUCCESS = "success"              # 成功
    FAILED = "failed"                # 失败
    MANUAL_REQUIRED = "manual_required"  # 需要手动输入


@dataclass
class LinkLearningRecord:
    """链接学习记录"""
    id: str
    url: str
    source_platform: str            # 来源平台
    learning_target: LearningTarget  # 学习目标
    notes: Optional[str] = None     # 备注
    status: LinkLearningStatus = LinkLearningStatus.PENDING
    
    # 提取结果
    extracted_title: Optional[str] = None
    extracted_key_points: List[str] = field(default_factory=list)
    extracted_keywords: List[str] = field(default_factory=list)
    extracted_price_info: Optional[str] = None
    page_structure: Optional[str] = None
    content_summary: Optional[str] = None
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "url": self.url,
            "source_platform": self.source_platform,
            "learning_target": self.learning_target.value,
            "notes": self.notes,
            "status": self.status.value,
            "extracted_title": self.extracted_title,
            "extracted_key_points": self.extracted_key_points,
            "extracted_keywords": self.extracted_keywords,
            "extracted_price_info": self.extracted_price_info,
            "page_structure": self.page_structure,
            "content_summary": self.content_summary,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class TextLearningRecord:
    """文本学习记录"""
    id: str
    title: str
    content: str
    category: str                  # 类目
    tags: List[str] = field(default_factory=list)
    learning_target: LearningTarget = LearningTarget.OTHER
    
    # 学习结果
    knowledge_summary: Optional[str] = None
    reusable_rules: List[str] = field(default_factory=list)
    extracted_keywords: List[str] = field(default_factory=list)
    operation_suggestions: List[str] = field(default_factory=list)
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "learning_target": self.learning_target.value,
            "knowledge_summary": self.knowledge_summary,
            "reusable_rules": self.reusable_rules,
            "extracted_keywords": self.extracted_keywords,
            "operation_suggestions": self.operation_suggestions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class TableLearningRecord:
    """表格学习记录"""
    id: str
    filename: str
    data_type: DataType            # 数据类型
    row_count: int = 0
    
    # 学习结果
    data_summary: Optional[str] = None
    abnormal_metrics: List[str] = field(default_factory=list)
    optimization_directions: List[str] = field(default_factory=list)
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "filename": self.filename,
            "data_type": self.data_type.value,
            "row_count": self.row_count,
            "data_summary": self.data_summary,
            "abnormal_metrics": self.abnormal_metrics,
            "optimization_directions": self.optimization_directions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ReviewLearningRecord:
    """复盘学习记录"""
    id: str
    action: str                    # 本次动作
    result: str                    # 执行结果
    exposure: Optional[int] = None     # 曝光
    click_rate: Optional[float] = None # 点击率
    conversion_rate: Optional[float] = None  # 转化率
    roi: Optional[float] = None    # ROI
    problems: List[str] = field(default_factory=list)
    next_action: Optional[str] = None  # 下一步动作
    
    # 学习结果
    experience_summary: Optional[str] = None  # 经验沉淀
    next_optimization_suggestions: List[str] = field(default_factory=list)
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "action": self.action,
            "result": self.result,
            "exposure": self.exposure,
            "click_rate": self.click_rate,
            "conversion_rate": self.conversion_rate,
            "roi": self.roi,
            "problems": self.problems,
            "next_action": self.next_action,
            "experience_summary": self.experience_summary,
            "next_optimization_suggestions": self.next_optimization_suggestions,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class KnowledgeRecord:
    """知识库记录"""
    id: str
    title: str
    content: str
    category: str
    tags: List[str] = field(default_factory=list)
    source_type: str = "manual"     # manual, link, text, table, review
    source_id: Optional[str] = None  # 来源记录ID
    
    # 应用场景
    applicable_scenarios: List[str] = field(default_factory=list)
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "category": self.category,
            "tags": self.tags,
            "source_type": self.source_type,
            "source_id": self.source_id,
            "applicable_scenarios": self.applicable_scenarios,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class MerchantProfile:
    """商家档案"""
    id: str
    merchant_name: str
    main_category: str            # 主营类目
    price_range: str              # 价格段
    positioning: str              # 店铺定位
    target_audience: str          # 目标人群
    platforms: List[str] = field(default_factory=list)  # 经营平台
    
    # 时间戳
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "id": self.id,
            "merchant_name": self.merchant_name,
            "main_category": self.main_category,
            "price_range": self.price_range,
            "positioning": self.positioning,
            "target_audience": self.target_audience,
            "platforms": self.platforms,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
