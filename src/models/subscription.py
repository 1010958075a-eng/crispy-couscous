"""
产品B v1.2 - 套餐额度中心/AI点数系统数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class PlanLevel(str, Enum):
    """套餐等级"""
    FREE = "free"
    BASIC = "basic"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class AccountStatus(str, Enum):
    """账户状态"""
    ACTIVE = "active"
    SUSPENDED = "suspended"
    CANCELLED = "cancelled"


class UsageStatus(str, Enum):
    """消费状态"""
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"


class FeatureType(str, Enum):
    """功能类型"""
    TEXT_GENERATION = "text_generation"
    IMAGE_GENERATION = "image_generation"
    WORKFLOW_EXECUTION = "workflow_execution"
    ADVANCED_ANALYSIS = "advanced_analysis"
    PROVIDER_MOCK_CALL = "provider_mock_call"


@dataclass
class SubscriptionPlan:
    """订阅套餐"""
    plan_id: str
    plan_name: str
    plan_level: str
    monthly_price: float
    included_points: int
    daily_point_limit: int
    monthly_point_limit: int
    image_generation_limit: int
    remove_bg_limit: int
    workflow_limit: int
    knowledge_base_limit: int
    advanced_model_enabled: bool
    team_member_limit: int
    private_deployment_enabled: bool
    enabled: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "plan_level": self.plan_level,
            "monthly_price": self.monthly_price,
            "included_points": self.included_points,
            "daily_point_limit": self.daily_point_limit,
            "monthly_point_limit": self.monthly_point_limit,
            "image_generation_limit": self.image_generation_limit,
            "remove_bg_limit": self.remove_bg_limit,
            "workflow_limit": self.workflow_limit,
            "knowledge_base_limit": self.knowledge_base_limit,
            "advanced_model_enabled": self.advanced_model_enabled,
            "team_member_limit": self.team_member_limit,
            "private_deployment_enabled": self.private_deployment_enabled,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class CustomerQuotaAccount:
    """客户额度账户"""
    account_id: str
    customer_id: str
    plan_id: str
    total_points: int
    used_points: int
    remaining_points: int
    daily_used_points: int
    monthly_used_points: int
    status: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "account_id": self.account_id,
            "customer_id": self.customer_id,
            "plan_id": self.plan_id,
            "total_points": self.total_points,
            "used_points": self.used_points,
            "remaining_points": self.remaining_points,
            "daily_used_points": self.daily_used_points,
            "monthly_used_points": self.monthly_used_points,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class FeaturePointRule:
    """功能扣点规则"""
    rule_id: str
    feature_name: str
    points_required: int
    feature_type: str
    risk_level: str
    enabled: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "rule_id": self.rule_id,
            "feature_name": self.feature_name,
            "points_required": self.points_required,
            "feature_type": self.feature_type,
            "risk_level": self.risk_level,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class UsageRecord:
    """消费记录"""
    usage_id: str
    customer_id: str
    account_id: str
    plan_id: str
    feature_name: str
    points_used: int
    status: str
    blocked_reason: Optional[str] = None
    before_remaining_points: int = 0
    after_remaining_points: int = 0
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "usage_id": self.usage_id,
            "customer_id": self.customer_id,
            "account_id": self.account_id,
            "plan_id": self.plan_id,
            "feature_name": self.feature_name,
            "points_used": self.points_used,
            "status": self.status,
            "blocked_reason": self.blocked_reason,
            "before_remaining_points": self.before_remaining_points,
            "after_remaining_points": self.after_remaining_points,
            "created_at": self.created_at.isoformat()
        }


# 内置套餐
BUILTIN_PLANS = [
    SubscriptionPlan(
        plan_id="free",
        plan_name="免费版",
        plan_level=PlanLevel.FREE.value,
        monthly_price=0.0,
        included_points=100,
        daily_point_limit=10,
        monthly_point_limit=100,
        image_generation_limit=5,
        remove_bg_limit=0,
        workflow_limit=1,
        knowledge_base_limit=1,
        advanced_model_enabled=False,
        team_member_limit=1,
        private_deployment_enabled=False,
        enabled=True
    ),
    SubscriptionPlan(
        plan_id="basic",
        plan_name="基础版",
        plan_level=PlanLevel.BASIC.value,
        monthly_price=29.0,
        included_points=1000,
        daily_point_limit=50,
        monthly_point_limit=1000,
        image_generation_limit=50,
        remove_bg_limit=10,
        workflow_limit=10,
        knowledge_base_limit=5,
        advanced_model_enabled=False,
        team_member_limit=3,
        private_deployment_enabled=False,
        enabled=True
    ),
    SubscriptionPlan(
        plan_id="pro",
        plan_name="专业版",
        plan_level=PlanLevel.PRO.value,
        monthly_price=99.0,
        included_points=10000,
        daily_point_limit=200,
        monthly_point_limit=10000,
        image_generation_limit=500,
        remove_bg_limit=100,
        workflow_limit=50,
        knowledge_base_limit=10,
        advanced_model_enabled=True,
        team_member_limit=10,
        private_deployment_enabled=False,
        enabled=True
    ),
    SubscriptionPlan(
        plan_id="enterprise",
        plan_name="企业版",
        plan_level=PlanLevel.ENTERPRISE.value,
        monthly_price=299.0,
        included_points=100000,
        daily_point_limit=1000,
        monthly_point_limit=100000,
        image_generation_limit=5000,
        remove_bg_limit=1000,
        workflow_limit=200,
        knowledge_base_limit=50,
        advanced_model_enabled=True,
        team_member_limit=50,
        private_deployment_enabled=True,
        enabled=True
    )
]

# 内置扣点规则
BUILTIN_FEATURE_RULES = [
    FeaturePointRule(
        rule_id="rule_title_generation",
        feature_name="title_generation",
        points_required=1,
        feature_type=FeatureType.TEXT_GENERATION.value,
        risk_level="low",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_keyword_generation",
        feature_name="keyword_generation",
        points_required=1,
        feature_type=FeatureType.TEXT_GENERATION.value,
        risk_level="low",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_xiaohongshu_generation",
        feature_name="xiaohongshu_generation",
        points_required=3,
        feature_type=FeatureType.TEXT_GENERATION.value,
        risk_level="low",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_video_script_generation",
        feature_name="video_script_generation",
        points_required=5,
        feature_type=FeatureType.TEXT_GENERATION.value,
        risk_level="medium",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_detail_page_generation",
        feature_name="detail_page_generation",
        points_required=10,
        feature_type=FeatureType.TEXT_GENERATION.value,
        risk_level="medium",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_workflow_execution",
        feature_name="workflow_execution",
        points_required=5,
        feature_type=FeatureType.WORKFLOW_EXECUTION.value,
        risk_level="medium",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_remove_bg",
        feature_name="remove_bg",
        points_required=10,
        feature_type=FeatureType.IMAGE_GENERATION.value,
        risk_level="low",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_image_generation",
        feature_name="image_generation",
        points_required=20,
        feature_type=FeatureType.IMAGE_GENERATION.value,
        risk_level="low",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_hd_image_generation",
        feature_name="hd_image_generation",
        points_required=50,
        feature_type=FeatureType.IMAGE_GENERATION.value,
        risk_level="medium",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_advanced_analysis",
        feature_name="advanced_analysis",
        points_required=20,
        feature_type=FeatureType.ADVANCED_ANALYSIS.value,
        risk_level="medium",
        enabled=True
    ),
    FeaturePointRule(
        rule_id="rule_provider_mock_call",
        feature_name="provider_mock_call",
        points_required=1,
        feature_type=FeatureType.PROVIDER_MOCK_CALL.value,
        risk_level="low",
        enabled=True
    )
]

# 高风险功能
HIGH_RISK_FEATURES = [
    "auto_login",
    "auto_publish",
    "auto_price_change",
    "auto_ad_spend",
    "auto_payment",
    "auto_deduction"
]
