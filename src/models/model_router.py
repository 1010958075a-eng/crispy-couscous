"""
产品B v1.3 - 模型路由中心 / 业务层 MoE 雏形数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class ModelTier(str, Enum):
    """模型等级"""
    LOW_COST = "low_cost"
    BALANCED = "balanced"
    HIGH_QUALITY = "high_quality"
    LOCAL_ONLY = "local_only"


class CostLevel(str, Enum):
    """成本等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class QualityLevel(str, Enum):
    """质量等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SpeedLevel(str, Enum):
    """速度等级"""
    FAST = "fast"
    MEDIUM = "medium"
    SLOW = "slow"


class PrivacyLevel(str, Enum):
    """隐私等级"""
    PUBLIC = "public"
    PRIVATE = "private"
    LOCAL_ONLY = "local_only"


class RoutePolicy(str, Enum):
    """路由策略"""
    COST_FIRST = "cost_first"
    QUALITY_FIRST = "quality_first"
    BALANCED = "balanced"
    SPEED_FIRST = "speed_first"
    PRIVACY_FIRST = "privacy_first"
    LOCAL_ONLY = "local_only"
    HIGH_RISK_GUARDED = "high_risk_guarded"


class TaskType(str, Enum):
    """任务类型"""
    TITLE_GENERATION = "title_generation"
    KEYWORD_GENERATION = "keyword_generation"
    XIAOHONGSHU_GENERATION = "xiaohongshu_generation"
    VIDEO_SCRIPT_GENERATION = "video_script_generation"
    DETAIL_PAGE_GENERATION = "detail_page_generation"
    IMAGE_PROMPT_GENERATION = "image_prompt_generation"
    REMOVE_BG = "remove_bg"
    WORKFLOW_EXECUTION = "workflow_execution"
    KNOWLEDGE_QA = "knowledge_qa"
    OPERATIONS_ANALYSIS = "operations_analysis"
    ADVANCED_ANALYSIS = "advanced_analysis"
    RISK_CHECK = "risk_check"
    UNKNOWN = "unknown"


class ExpertType(str, Enum):
    """专家类型"""
    DOMAIN = "domain"
    QUALITY = "quality"
    COST = "cost"
    RISK = "risk"
    PRIVACY = "privacy"
    APPROVAL = "approval"


@dataclass
class ModelProfile:
    """模型档案"""
    model_id: str
    provider_id: str
    model_name: str
    provider_type: str
    model_tier: str
    capability_tags: List[str]
    supported_task_types: List[str]
    cost_level: str
    quality_level: str
    speed_level: str
    privacy_level: str
    supports_local_only: bool
    supports_streaming: bool
    supports_batch: bool
    supports_rag: bool
    supports_image: bool
    supports_text: bool
    enabled: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "model_id": self.model_id,
            "provider_id": self.provider_id,
            "model_name": self.model_name,
            "provider_type": self.provider_type,
            "model_tier": self.model_tier,
            "capability_tags": self.capability_tags,
            "supported_task_types": self.supported_task_types,
            "cost_level": self.cost_level,
            "quality_level": self.quality_level,
            "speed_level": self.speed_level,
            "privacy_level": self.privacy_level,
            "supports_local_only": self.supports_local_only,
            "supports_streaming": self.supports_streaming,
            "supports_batch": self.supports_batch,
            "supports_rag": self.supports_rag,
            "supports_image": self.supports_image,
            "supports_text": self.supports_text,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class BusinessExpert:
    """业务专家"""
    expert_id: str
    expert_name: str
    expert_type: str
    supported_task_types: List[str]
    capability_tags: List[str]
    risk_level: str
    default_priority: int
    enabled: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "expert_id": self.expert_id,
            "expert_name": self.expert_name,
            "expert_type": self.expert_type,
            "supported_task_types": self.supported_task_types,
            "capability_tags": self.capability_tags,
            "risk_level": self.risk_level,
            "default_priority": self.default_priority,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ModelRouteRule:
    """模型路由规则"""
    rule_id: str
    task_type: str
    feature_name: str
    route_policy: str
    preferred_expert_ids: List[str]
    preferred_model_ids: List[str]
    fallback_model_ids: List[str]
    min_quality_level: Optional[str] = None
    max_cost_level: Optional[str] = None
    local_only_required: bool = False
    human_approval_required: bool = False
    enabled: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "rule_id": self.rule_id,
            "task_type": self.task_type,
            "feature_name": self.feature_name,
            "route_policy": self.route_policy,
            "preferred_expert_ids": self.preferred_expert_ids,
            "preferred_model_ids": self.preferred_model_ids,
            "fallback_model_ids": self.fallback_model_ids,
            "min_quality_level": self.min_quality_level,
            "max_cost_level": self.max_cost_level,
            "local_only_required": self.local_only_required,
            "human_approval_required": self.human_approval_required,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ModelRouteDecision:
    """模型路由决策记录"""
    decision_id: str
    task_text: str
    task_type: str
    feature_name: Optional[str]
    customer_id: Optional[str]
    account_id: Optional[str]
    route_policy: str
    selected_expert_ids: List[str]
    candidate_model_ids: List[str]
    selected_model_id: Optional[str]
    fallback_model_ids: List[str]
    estimated_points: int
    estimated_cost_level: str
    requires_human_approval: bool
    status: str
    blocked_reason: Optional[str]
    decision_reason: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "decision_id": self.decision_id,
            "task_text": self.task_text,
            "task_type": self.task_type,
            "feature_name": self.feature_name,
            "customer_id": self.customer_id,
            "account_id": self.account_id,
            "route_policy": self.route_policy,
            "selected_expert_ids": self.selected_expert_ids,
            "candidate_model_ids": self.candidate_model_ids,
            "selected_model_id": self.selected_model_id,
            "fallback_model_ids": self.fallback_model_ids,
            "estimated_points": self.estimated_points,
            "estimated_cost_level": self.estimated_cost_level,
            "requires_human_approval": self.requires_human_approval,
            "status": self.status,
            "blocked_reason": self.blocked_reason,
            "decision_reason": self.decision_reason,
            "created_at": self.created_at.isoformat()
        }


# 内置模型档案
BUILTIN_MODEL_PROFILES = [
    ModelProfile(
        model_id="openai_low_cost_text",
        provider_id="openai_text",
        model_name="gpt-3.5-turbo",
        provider_type="text_model",
        model_tier=ModelTier.LOW_COST.value,
        capability_tags=["text_generation", "translation", "summarization"],
        supported_task_types=[
            TaskType.TITLE_GENERATION.value,
            TaskType.KEYWORD_GENERATION.value,
            TaskType.XIAOHONGSHU_GENERATION.value,
            TaskType.VIDEO_SCRIPT_GENERATION.value
        ],
        cost_level=CostLevel.LOW.value,
        quality_level=QualityLevel.MEDIUM.value,
        speed_level=SpeedLevel.FAST.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=True,
        supports_batch=True,
        supports_rag=False,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="openai_high_quality_text",
        provider_id="openai_text",
        model_name="gpt-4",
        provider_type="text_model",
        model_tier=ModelTier.HIGH_QUALITY.value,
        capability_tags=["text_generation", "translation", "summarization", "analysis"],
        supported_task_types=[
            TaskType.DETAIL_PAGE_GENERATION.value,
            TaskType.OPERATIONS_ANALYSIS.value,
            TaskType.ADVANCED_ANALYSIS.value
        ],
        cost_level=CostLevel.HIGH.value,
        quality_level=QualityLevel.HIGH.value,
        speed_level=SpeedLevel.SLOW.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=True,
        supports_batch=True,
        supports_rag=False,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="qwen_low_cost_text",
        provider_id="qwen_text",
        model_name="qwen-turbo",
        provider_type="text_model",
        model_tier=ModelTier.LOW_COST.value,
        capability_tags=["text_generation", "translation", "summarization"],
        supported_task_types=[
            TaskType.TITLE_GENERATION.value,
            TaskType.KEYWORD_GENERATION.value,
            TaskType.XIAOHONGSHU_GENERATION.value
        ],
        cost_level=CostLevel.LOW.value,
        quality_level=QualityLevel.MEDIUM.value,
        speed_level=SpeedLevel.FAST.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=True,
        supports_batch=True,
        supports_rag=False,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="qwen_balanced_text",
        provider_id="qwen_text",
        model_name="qwen-plus",
        provider_type="text_model",
        model_tier=ModelTier.BALANCED.value,
        capability_tags=["text_generation", "translation", "summarization", "analysis"],
        supported_task_types=[
            TaskType.DETAIL_PAGE_GENERATION.value,
            TaskType.VIDEO_SCRIPT_GENERATION.value,
            TaskType.OPERATIONS_ANALYSIS.value
        ],
        cost_level=CostLevel.MEDIUM.value,
        quality_level=QualityLevel.HIGH.value,
        speed_level=SpeedLevel.MEDIUM.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=True,
        supports_batch=True,
        supports_rag=False,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="dify_knowledge_router",
        provider_id="dify_knowledge",
        model_name="dify-knowledge",
        provider_type="knowledge_base",
        model_tier=ModelTier.BALANCED.value,
        capability_tags=["rag", "knowledge_qa"],
        supported_task_types=[
            TaskType.KNOWLEDGE_QA.value
        ],
        cost_level=CostLevel.MEDIUM.value,
        quality_level=QualityLevel.MEDIUM.value,
        speed_level=SpeedLevel.MEDIUM.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=True,
        supports_batch=True,
        supports_rag=True,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="ollama_qwen_local_mock",
        provider_id="ollama_local",
        model_name="qwen2.5-7b",
        provider_type="local_model",
        model_tier=ModelTier.LOCAL_ONLY.value,
        capability_tags=["text_generation", "translation", "summarization"],
        supported_task_types=[
            TaskType.TITLE_GENERATION.value,
            TaskType.KEYWORD_GENERATION.value,
            TaskType.DETAIL_PAGE_GENERATION.value
        ],
        cost_level=CostLevel.LOW.value,
        quality_level=QualityLevel.MEDIUM.value,
        speed_level=SpeedLevel.MEDIUM.value,
        privacy_level=PrivacyLevel.LOCAL_ONLY.value,
        supports_local_only=True,
        supports_streaming=True,
        supports_batch=False,
        supports_rag=False,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="vllm_qwen_local_mock",
        provider_id="ollama_local",
        model_name="qwen2.5-14b",
        provider_type="local_model",
        model_tier=ModelTier.LOCAL_ONLY.value,
        capability_tags=["text_generation", "translation", "summarization", "analysis"],
        supported_task_types=[
            TaskType.DETAIL_PAGE_GENERATION.value,
            TaskType.OPERATIONS_ANALYSIS.value,
            TaskType.ADVANCED_ANALYSIS.value
        ],
        cost_level=CostLevel.LOW.value,
        quality_level=QualityLevel.HIGH.value,
        speed_level=SpeedLevel.MEDIUM.value,
        privacy_level=PrivacyLevel.LOCAL_ONLY.value,
        supports_local_only=True,
        supports_streaming=True,
        supports_batch=True,
        supports_rag=False,
        supports_image=False,
        supports_text=True,
        enabled=True
    ),
    ModelProfile(
        model_id="wanxiang_image_mock",
        provider_id="wanxiang_image",
        model_name="wanxiang-image",
        provider_type="image_model",
        model_tier=ModelTier.BALANCED.value,
        capability_tags=["image_generation"],
        supported_task_types=[
            TaskType.IMAGE_PROMPT_GENERATION.value
        ],
        cost_level=CostLevel.MEDIUM.value,
        quality_level=QualityLevel.HIGH.value,
        speed_level=SpeedLevel.SLOW.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=False,
        supports_batch=True,
        supports_rag=False,
        supports_image=True,
        supports_text=False,
        enabled=True
    ),
    ModelProfile(
        model_id="remove_bg_mock",
        provider_id="remove_bg",
        model_name="remove-bg-service",
        provider_type="image_remove_bg",
        model_tier=ModelTier.LOW_COST.value,
        capability_tags=["remove_bg"],
        supported_task_types=[
            TaskType.REMOVE_BG.value
        ],
        cost_level=CostLevel.LOW.value,
        quality_level=QualityLevel.MEDIUM.value,
        speed_level=SpeedLevel.FAST.value,
        privacy_level=PrivacyLevel.PRIVATE.value,
        supports_local_only=False,
        supports_streaming=False,
        supports_batch=True,
        supports_rag=False,
        supports_image=True,
        supports_text=False,
        enabled=True
    )
]

# 内置业务专家
BUILTIN_BUSINESS_EXPERTS = [
    BusinessExpert(
        expert_id="title_expert",
        expert_name="标题生成专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.TITLE_GENERATION.value
        ],
        capability_tags=["title", "marketing", "seo"],
        risk_level="low",
        default_priority=1,
        enabled=True
    ),
    BusinessExpert(
        expert_id="keyword_expert",
        expert_name="关键词生成专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.KEYWORD_GENERATION.value
        ],
        capability_tags=["keyword", "marketing", "seo"],
        risk_level="low",
        default_priority=1,
        enabled=True
    ),
    BusinessExpert(
        expert_id="detail_page_expert",
        expert_name="详情页生成专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.DETAIL_PAGE_GENERATION.value
        ],
        capability_tags=["detail", "marketing", "sales"],
        risk_level="medium",
        default_priority=2,
        enabled=True
    ),
    BusinessExpert(
        expert_id="visual_prompt_expert",
        expert_name="视觉提示词专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.IMAGE_PROMPT_GENERATION.value
        ],
        capability_tags=["visual", "image", "prompt"],
        risk_level="low",
        default_priority=2,
        enabled=True
    ),
    BusinessExpert(
        expert_id="xiaohongshu_expert",
        expert_name="小红书生成专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.XIAOHONGSHU_GENERATION.value
        ],
        capability_tags=["xiaohongshu", "social", "content"],
        risk_level="low",
        default_priority=1,
        enabled=True
    ),
    BusinessExpert(
        expert_id="video_script_expert",
        expert_name="视频脚本生成专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.VIDEO_SCRIPT_GENERATION.value
        ],
        capability_tags=["video", "script", "content"],
        risk_level="medium",
        default_priority=2,
        enabled=True
    ),
    BusinessExpert(
        expert_id="operations_analysis_expert",
        expert_name="运营分析专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.OPERATIONS_ANALYSIS.value,
            TaskType.ADVANCED_ANALYSIS.value
        ],
        capability_tags=["analysis", "operations", "data"],
        risk_level="medium",
        default_priority=3,
        enabled=True
    ),
    BusinessExpert(
        expert_id="knowledge_base_expert",
        expert_name="知识库专家",
        expert_type=ExpertType.DOMAIN.value,
        supported_task_types=[
            TaskType.KNOWLEDGE_QA.value
        ],
        capability_tags=["knowledge", "rag", "qa"],
        risk_level="low",
        default_priority=2,
        enabled=True
    ),
    BusinessExpert(
        expert_id="risk_control_expert",
        expert_name="风控专家",
        expert_type=ExpertType.RISK.value,
        supported_task_types=[
            TaskType.RISK_CHECK.value
        ],
        capability_tags=["risk", "security", "compliance"],
        risk_level="high",
        default_priority=4,
        enabled=True
    ),
    BusinessExpert(
        expert_id="cost_control_expert",
        expert_name="成本控制专家",
        expert_type=ExpertType.COST.value,
        supported_task_types=[
            TaskType.TITLE_GENERATION.value,
            TaskType.KEYWORD_GENERATION.value,
            TaskType.XIAOHONGSHU_GENERATION.value
        ],
        capability_tags=["cost", "optimization", "budget"],
        risk_level="low",
        default_priority=1,
        enabled=True
    ),
    BusinessExpert(
        expert_id="approval_gate_expert",
        expert_name="审批闸门专家",
        expert_type=ExpertType.APPROVAL.value,
        supported_task_types=[
            TaskType.DETAIL_PAGE_GENERATION.value,
            TaskType.OPERATIONS_ANALYSIS.value,
            TaskType.ADVANCED_ANALYSIS.value
        ],
        capability_tags=["approval", "review", "gate"],
        risk_level="high",
        default_priority=5,
        enabled=True
    ),
    BusinessExpert(
        expert_id="local_privacy_expert",
        expert_name="本地隐私专家",
        expert_type=ExpertType.PRIVACY.value,
        supported_task_types=[
            TaskType.TITLE_GENERATION.value,
            TaskType.KEYWORD_GENERATION.value,
            TaskType.DETAIL_PAGE_GENERATION.value
        ],
        capability_tags=["privacy", "local", "data_protection"],
        risk_level="low",
        default_priority=3,
        enabled=True
    )
]

# 内置路由规则
BUILTIN_ROUTE_RULES = [
    ModelRouteRule(
        rule_id="rule_title_generation",
        task_type=TaskType.TITLE_GENERATION.value,
        feature_name="title_generation",
        route_policy=RoutePolicy.COST_FIRST.value,
        preferred_expert_ids=["title_expert", "cost_control_expert"],
        preferred_model_ids=["qwen_low_cost_text", "openai_low_cost_text"],
        fallback_model_ids=["ollama_qwen_local_mock"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.LOW.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_keyword_generation",
        task_type=TaskType.KEYWORD_GENERATION.value,
        feature_name="keyword_generation",
        route_policy=RoutePolicy.COST_FIRST.value,
        preferred_expert_ids=["keyword_expert", "cost_control_expert"],
        preferred_model_ids=["qwen_low_cost_text", "openai_low_cost_text"],
        fallback_model_ids=["ollama_qwen_local_mock"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.LOW.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_detail_page_generation",
        task_type=TaskType.DETAIL_PAGE_GENERATION.value,
        feature_name="detail_page_generation",
        route_policy=RoutePolicy.QUALITY_FIRST.value,
        preferred_expert_ids=["detail_page_expert", "approval_gate_expert"],
        preferred_model_ids=["qwen_balanced_text", "openai_high_quality_text"],
        fallback_model_ids=["vllm_qwen_local_mock"],
        min_quality_level=QualityLevel.HIGH.value,
        max_cost_level=CostLevel.HIGH.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_operations_analysis",
        task_type=TaskType.OPERATIONS_ANALYSIS.value,
        feature_name="operations_analysis",
        route_policy=RoutePolicy.QUALITY_FIRST.value,
        preferred_expert_ids=["operations_analysis_expert", "approval_gate_expert"],
        preferred_model_ids=["qwen_balanced_text", "openai_high_quality_text"],
        fallback_model_ids=["vllm_qwen_local_mock"],
        min_quality_level=QualityLevel.HIGH.value,
        max_cost_level=CostLevel.HIGH.value,
        local_only_required=False,
        human_approval_required=True,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_local_only",
        task_type=TaskType.TITLE_GENERATION.value,
        feature_name="title_generation",
        route_policy=RoutePolicy.LOCAL_ONLY.value,
        preferred_expert_ids=["local_privacy_expert", "title_expert"],
        preferred_model_ids=["ollama_qwen_local_mock", "vllm_qwen_local_mock"],
        fallback_model_ids=[],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.LOW.value,
        local_only_required=True,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_risk_guarded",
        task_type=TaskType.ADVANCED_ANALYSIS.value,
        feature_name="advanced_analysis",
        route_policy=RoutePolicy.HIGH_RISK_GUARDED.value,
        preferred_expert_ids=["risk_control_expert", "approval_gate_expert"],
        preferred_model_ids=["openai_high_quality_text", "qwen_balanced_text"],
        fallback_model_ids=[],
        min_quality_level=QualityLevel.HIGH.value,
        max_cost_level=CostLevel.HIGH.value,
        local_only_required=False,
        human_approval_required=True,
        enabled=True
    ),
    # 新增缺失的默认路由规则
    ModelRouteRule(
        rule_id="rule_knowledge_qa",
        task_type=TaskType.KNOWLEDGE_QA.value,
        feature_name="knowledge_qa",
        route_policy=RoutePolicy.BALANCED.value,
        preferred_expert_ids=["knowledge_base_expert"],
        preferred_model_ids=["dify_knowledge_router", "qwen_balanced_text"],
        fallback_model_ids=["qwen_low_cost_text"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.MEDIUM.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_image_prompt_generation",
        task_type=TaskType.IMAGE_PROMPT_GENERATION.value,
        feature_name="image_prompt_generation",
        route_policy=RoutePolicy.BALANCED.value,
        preferred_expert_ids=["visual_prompt_expert"],
        preferred_model_ids=["qwen_balanced_text", "openai_low_cost_text"],
        fallback_model_ids=["wanxiang_image_mock"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.MEDIUM.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_workflow_execution",
        task_type=TaskType.WORKFLOW_EXECUTION.value,
        feature_name="workflow_execution",
        route_policy=RoutePolicy.COST_FIRST.value,
        preferred_expert_ids=["cost_control_expert", "approval_gate_expert"],
        preferred_model_ids=["qwen_low_cost_text", "openai_low_cost_text"],
        fallback_model_ids=["ollama_qwen_local_mock"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.LOW.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_risk_check",
        task_type=TaskType.RISK_CHECK.value,
        feature_name="risk_check",
        route_policy=RoutePolicy.HIGH_RISK_GUARDED.value,
        preferred_expert_ids=["risk_control_expert", "approval_gate_expert"],
        preferred_model_ids=["qwen_low_cost_text", "openai_low_cost_text"],
        fallback_model_ids=[],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.LOW.value,
        local_only_required=False,
        human_approval_required=True,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_xiaohongshu_generation",
        task_type=TaskType.XIAOHONGSHU_GENERATION.value,
        feature_name="xiaohongshu_generation",
        route_policy=RoutePolicy.COST_FIRST.value,
        preferred_expert_ids=["xiaohongshu_expert"],
        preferred_model_ids=["qwen_balanced_text", "openai_low_cost_text"],
        fallback_model_ids=["qwen_low_cost_text"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.MEDIUM.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_video_script_generation",
        task_type=TaskType.VIDEO_SCRIPT_GENERATION.value,
        feature_name="video_script_generation",
        route_policy=RoutePolicy.BALANCED.value,
        preferred_expert_ids=["video_script_expert"],
        preferred_model_ids=["qwen_balanced_text", "openai_low_cost_text"],
        fallback_model_ids=["qwen_low_cost_text"],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.MEDIUM.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_remove_bg",
        task_type=TaskType.REMOVE_BG.value,
        feature_name="remove_bg",
        route_policy=RoutePolicy.COST_FIRST.value,
        preferred_expert_ids=["visual_prompt_expert", "cost_control_expert"],
        preferred_model_ids=["remove_bg_mock"],
        fallback_model_ids=[],
        min_quality_level=QualityLevel.MEDIUM.value,
        max_cost_level=CostLevel.LOW.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    ),
    ModelRouteRule(
        rule_id="rule_advanced_analysis",
        task_type=TaskType.ADVANCED_ANALYSIS.value,
        feature_name="advanced_analysis",
        route_policy=RoutePolicy.QUALITY_FIRST.value,
        preferred_expert_ids=["operations_analysis_expert", "cost_control_expert"],
        preferred_model_ids=["openai_high_quality_text", "qwen_balanced_text"],
        fallback_model_ids=["vllm_qwen_local_mock"],
        min_quality_level=QualityLevel.HIGH.value,
        max_cost_level=CostLevel.HIGH.value,
        local_only_required=False,
        human_approval_required=False,
        enabled=True
    )
]

# 高风险功能列表
HIGH_RISK_FEATURES = [
    "auto_login",
    "auto_publish",
    "auto_price_change",
    "auto_ad_spend",
    "auto_payment",
    "auto_deduction"
]
