"""
产品B v1.1 - API供应商中心数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class ProviderType(str, Enum):
    """供应商类型"""
    TEXT_MODEL = "text_model"
    IMAGE_MODEL = "image_model"
    IMAGE_REMOVE_BG = "image_remove_bg"
    KNOWLEDGE_BASE = "knowledge_base"
    WORKFLOW = "workflow"
    NOTIFICATION = "notification"
    ECOMMERCE = "ecommerce"
    LOCAL_MODEL = "local_model"


class CostLevel(str, Enum):
    """成本等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class RiskLevel(str, Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    RESTRICTED = "restricted"


class CallStatus(str, Enum):
    """调用状态"""
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class ApiProvider:
    """API供应商配置"""
    provider_id: str
    provider_name: str
    provider_type: str
    model_name: Optional[str]
    api_base_url: Optional[str]
    api_key_placeholder: Optional[str]
    cost_level: str
    risk_level: str
    enabled: bool
    daily_limit: int
    monthly_limit: int
    used_today: int = 0
    used_this_month: int = 0
    unit_cost_estimate: float = 0.0
    supported_features: List[str] = field(default_factory=list)
    fallback_provider_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "provider_type": self.provider_type,
            "model_name": self.model_name,
            "api_base_url": self.api_base_url,
            "api_key_placeholder": self.api_key_placeholder,
            "cost_level": self.cost_level,
            "risk_level": self.risk_level,
            "enabled": self.enabled,
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "used_today": self.used_today,
            "used_this_month": self.used_this_month,
            "unit_cost_estimate": self.unit_cost_estimate,
            "supported_features": self.supported_features,
            "fallback_provider_id": self.fallback_provider_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ApiCallRecord:
    """API调用记录"""
    call_id: str
    provider_id: str
    provider_name: str
    provider_type: str
    feature_name: str
    request_summary: str
    estimated_units: int
    estimated_cost: float
    status: str
    blocked_reason: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "call_id": self.call_id,
            "provider_id": self.provider_id,
            "provider_name": self.provider_name,
            "provider_type": self.provider_type,
            "feature_name": self.feature_name,
            "request_summary": self.request_summary,
            "estimated_units": self.estimated_units,
            "estimated_cost": self.estimated_cost,
            "status": self.status,
            "blocked_reason": self.blocked_reason,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class ApiQuotaRecord:
    """API额度记录"""
    quota_id: str
    provider_id: str
    daily_limit: int
    monthly_limit: int
    used_today: int
    used_this_month: int
    remaining_today: int
    remaining_this_month: int
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "quota_id": self.quota_id,
            "provider_id": self.provider_id,
            "daily_limit": self.daily_limit,
            "monthly_limit": self.monthly_limit,
            "used_today": self.used_today,
            "used_this_month": self.used_this_month,
            "remaining_today": self.remaining_today,
            "remaining_this_month": self.remaining_this_month,
            "updated_at": self.updated_at.isoformat()
        }


# 内置供应商配置
BUILTIN_PROVIDERS = [
    ApiProvider(
        provider_id="openai_text",
        provider_name="OpenAI 文本模型",
        provider_type=ProviderType.TEXT_MODEL.value,
        model_name="gpt-3.5-turbo",
        api_base_url="https://api.openai.com/v1",
        api_key_placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx",
        cost_level=CostLevel.HIGH.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=1000,
        monthly_limit=30000,
        unit_cost_estimate=0.002,
        supported_features=["text_generation", "summarization", "translation"]
    ),
    ApiProvider(
        provider_id="qwen_text",
        provider_name="通义千问文本模型",
        provider_type=ProviderType.TEXT_MODEL.value,
        model_name="qwen-turbo",
        api_base_url="https://dashscope.aliyuncs.com/api/v1",
        api_key_placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx",
        cost_level=CostLevel.LOW.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=2000,
        monthly_limit=60000,
        unit_cost_estimate=0.0008,
        supported_features=["text_generation", "summarization", "translation"]
    ),
    ApiProvider(
        provider_id="dify_knowledge",
        provider_name="Dify 知识库",
        provider_type=ProviderType.KNOWLEDGE_BASE.value,
        model_name=None,
        api_base_url="https://api.dify.ai/v1",
        api_key_placeholder="app-xxxxxxxxxxxxxxxxxxxxxxxx",
        cost_level=CostLevel.MEDIUM.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=500,
        monthly_limit=15000,
        unit_cost_estimate=0.001,
        supported_features=["knowledge_retrieval", "rag"]
    ),
    ApiProvider(
        provider_id="remove_bg",
        provider_name="Remove.bg 背景移除",
        provider_type=ProviderType.IMAGE_REMOVE_BG.value,
        model_name=None,
        api_base_url="https://api.remove.bg/v1.0",
        api_key_placeholder="xxxxxxxxxxxxxxxxxxxxxxxx",
        cost_level=CostLevel.HIGH.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=100,
        monthly_limit=3000,
        unit_cost_estimate=0.02,
        supported_features=["background_removal"]
    ),
    ApiProvider(
        provider_id="qwen_image",
        provider_name="通义万相图像",
        provider_type=ProviderType.IMAGE_MODEL.value,
        model_name="wanxiang-v1",
        api_base_url="https://dashscope.aliyuncs.com/api/v1",
        api_key_placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx",
        cost_level=CostLevel.MEDIUM.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=200,
        monthly_limit=6000,
        unit_cost_estimate=0.005,
        supported_features=["image_generation", "image_editing"]
    ),
    ApiProvider(
        provider_id="wanxiang_image",
        provider_name="万相图像",
        provider_type=ProviderType.IMAGE_MODEL.value,
        model_name="wanxiang-v2",
        api_base_url="https://wanxiang.alibaba.com/api/v1",
        api_key_placeholder="ak-xxxxxxxxxxxxxxxxxxxxxxxx",
        cost_level=CostLevel.MEDIUM.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=200,
        monthly_limit=6000,
        unit_cost_estimate=0.005,
        supported_features=["image_generation", "image_editing"]
    ),
    ApiProvider(
        provider_id="n8n_webhook",
        provider_name="n8n Webhook",
        provider_type=ProviderType.WORKFLOW.value,
        model_name=None,
        api_base_url="https://n8n.example.com/webhook",
        api_key_placeholder=None,
        cost_level=CostLevel.LOW.value,
        risk_level=RiskLevel.MEDIUM.value,
        enabled=True,
        daily_limit=1000,
        monthly_limit=30000,
        unit_cost_estimate=0.0,
        supported_features=["workflow_automation", "webhook_trigger"]
    ),
    ApiProvider(
        provider_id="ollama_local",
        provider_name="Ollama 本地模型",
        provider_type=ProviderType.LOCAL_MODEL.value,
        model_name="llama2",
        api_base_url="http://localhost:11434",
        api_key_placeholder=None,
        cost_level=CostLevel.LOW.value,
        risk_level=RiskLevel.LOW.value,
        enabled=True,
        daily_limit=5000,
        monthly_limit=150000,
        unit_cost_estimate=0.0,
        supported_features=["text_generation", "summarization", "translation"]
    )
]

# 高风险关键词
HIGH_RISK_KEYWORDS = [
    "自动登录",
    "自动上架",
    "自动改价",
    "自动开车",
    "开车投放",
    "自动投放",
    "自动扣费",
    "保存账号密码"
]

# 高风险供应商类型
HIGH_RISK_PROVIDER_TYPES = [
    "ecommerce",
    "payment",
    "ad_spend",
    "auto_publish",
    "auto_price_change"
]
