"""
产品B v0.7 - 工具中心数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class ToolType(str, Enum):
    """工具类型"""
    GENERATOR = "generator"
    CHECKER = "checker"
    MANAGER = "manager"
    EXECUTOR = "executor"


class ToolCategory(str, Enum):
    """工具分类"""
    CONTENT_GENERATION = "content_generation"
    TASK_MANAGEMENT = "task_management"
    ACCEPTANCE = "acceptance"
    RISK_CHECK = "risk_check"
    AUTOMATION = "automation"


class RiskLevel(str, Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class PlanStatus(str, Enum):
    """计划状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"


@dataclass
class Tool:
    """工具"""
    tool_id: str
    tool_name: str
    tool_category: str
    tool_type: str
    description: str
    related_module: str
    related_api: str
    input_requirements: List[str]
    output_description: str
    risk_level: str
    requires_human_confirmation: bool
    enabled: bool
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "tool_category": self.tool_category,
            "tool_type": self.tool_type,
            "description": self.description,
            "related_module": self.related_module,
            "related_api": self.related_api,
            "input_requirements": self.input_requirements,
            "output_description": self.output_description,
            "risk_level": self.risk_level,
            "requires_human_confirmation": self.requires_human_confirmation,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }


@dataclass
class ExecutionStep:
    """执行步骤"""
    step_number: int
    step_name: str
    tool_id: str
    tool_name: str
    reason: str
    expected_output: str
    risk_level: str
    requires_human_confirmation: bool

    def to_dict(self):
        """转换为字典"""
        return {
            "step_number": self.step_number,
            "step_name": self.step_name,
            "tool_id": self.tool_id,
            "tool_name": self.tool_name,
            "reason": self.reason,
            "expected_output": self.expected_output,
            "risk_level": self.risk_level,
            "requires_human_confirmation": self.requires_human_confirmation
        }


@dataclass
class ToolPlan:
    """工具调用计划"""
    plan_id: str
    original_request: str
    task_id: Optional[str]
    recommended_tools: List[str]
    execution_steps: List[ExecutionStep]
    risk_level: str
    human_confirmation_required: bool
    blocked_actions: List[str]
    plan_status: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "plan_id": self.plan_id,
            "original_request": self.original_request,
            "task_id": self.task_id,
            "recommended_tools": self.recommended_tools,
            "execution_steps": [step.to_dict() for step in self.execution_steps],
            "risk_level": self.risk_level,
            "human_confirmation_required": self.human_confirmation_required,
            "blocked_actions": self.blocked_actions,
            "plan_status": self.plan_status,
            "created_at": self.created_at.isoformat()
        }


# 内置工具注册表
BUILTIN_TOOLS = [
    Tool(
        tool_id="title_generator",
        tool_name="标题生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成20个淘宝/天猫标题",
        related_module="v0.3",
        related_api="/api/listing/generate-title",
        input_requirements=["product_id", "product_info"],
        output_description="20个标题列表",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="keyword_generator",
        tool_name="关键词生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成关键词包",
        related_module="v0.3",
        related_api="/api/listing/generate-keywords",
        input_requirements=["product_id", "product_info"],
        output_description="关键词包",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="main_image_prompt_generator",
        tool_name="主图提示词生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成主图九宫格AI提示词",
        related_module="v0.3",
        related_api="/api/listing/generate-main-image-prompts",
        input_requirements=["product_id", "product_info"],
        output_description="9个主图提示词",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="listing_package_generator",
        tool_name="上架包生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成上架基础包",
        related_module="v0.3",
        related_api="/api/listing/generate-package",
        input_requirements=["product_id", "product_info"],
        output_description="上架基础包（标题、关键词、主图提示词）",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="detail_screen_generator",
        tool_name="详情页生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成详情页9屏",
        related_module="v0.4",
        related_api="/api/detail/generate-9screens",
        input_requirements=["product_id", "product_info"],
        output_description="详情页9屏",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="video_script_generator",
        tool_name="短视频脚本生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成短视频脚本",
        related_module="v0.4",
        related_api="/api/content/generate-video-script",
        input_requirements=["product_id", "product_info"],
        output_description="短视频脚本",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="xiaohongshu_generator",
        tool_name="小红书文案生成器",
        tool_category=ToolCategory.CONTENT_GENERATION.value,
        tool_type=ToolType.GENERATOR.value,
        description="生成小红书文案",
        related_module="v0.4",
        related_api="/api/content/generate-xiaohongshu",
        input_requirements=["product_id", "product_info"],
        output_description="小红书文案",
        risk_level=RiskLevel.LOW.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="task_center",
        tool_name="任务中心",
        tool_category=ToolCategory.TASK_MANAGEMENT.value,
        tool_type=ToolType.MANAGER.value,
        description="创建任务、拆解任务、更新任务状态",
        related_module="v0.5",
        related_api="/api/tasks/create",
        input_requirements=["original_request", "product_id"],
        output_description="任务记录",
        risk_level=RiskLevel.MEDIUM.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="acceptance_checker",
        tool_name="验收检查器",
        tool_category=ToolCategory.ACCEPTANCE.value,
        tool_type=ToolType.CHECKER.value,
        description="检查任务、上架包、字段完整性",
        related_module="v0.6",
        related_api="/api/acceptance/check-task",
        input_requirements=["task_data", "package_data"],
        output_description="验收报告",
        risk_level=RiskLevel.MEDIUM.value,
        requires_human_confirmation=False,
        enabled=True
    ),
    Tool(
        tool_id="risk_checker",
        tool_name="风险检查器",
        tool_category=ToolCategory.RISK_CHECK.value,
        tool_type=ToolType.CHECKER.value,
        description="识别高风险动作",
        related_module="v0.6",
        related_api="/api/acceptance/check-risk",
        input_requirements=["text", "task_data"],
        output_description="风险识别结果",
        risk_level=RiskLevel.MEDIUM.value,
        requires_human_confirmation=False,
        enabled=True
    )
]
