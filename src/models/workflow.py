"""
产品B v0.8 - 工作流中心数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from enum import Enum


class WorkflowStatus(str, Enum):
    """工作流状态"""
    PENDING = "pending"
    RUNNING = "running"
    WAITING_CONFIRMATION = "waiting_confirmation"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    FAILED = "failed"


class StepStatus(str, Enum):
    """步骤状态"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class StepType(str, Enum):
    """步骤类型"""
    TASK_CREATION = "task_creation"
    TOOL_RECOMMENDATION = "tool_recommendation"
    TOOL_PLAN_GENERATION = "tool_plan_generation"
    CONTENT_GENERATION = "content_generation"
    ACCEPTANCE_CHECK = "acceptance_check"
    RISK_CHECK = "risk_check"
    MANUAL_CONFIRMATION = "manual_confirmation"
    ARCHIVE = "archive"


@dataclass
class WorkflowStep:
    """工作流步骤"""
    step_number: int
    step_name: str
    step_type: str
    description: str
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None

    def to_dict(self):
        """转换为字典"""
        return {
            "step_number": self.step_number,
            "step_name": self.step_name,
            "step_type": self.step_type,
            "description": self.description,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error_message": self.error_message
        }


@dataclass
class Workflow:
    """工作流记录"""
    workflow_id: str
    original_request: str
    task_id: Optional[str]
    workflow_status: str
    risk_level: str
    human_confirmation_required: bool
    blocked_actions: List[str]
    steps: List[WorkflowStep]
    current_step_number: int
    confirmed_by: Optional[str] = None
    confirmed_at: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "workflow_id": self.workflow_id,
            "original_request": self.original_request,
            "task_id": self.task_id,
            "workflow_status": self.workflow_status,
            "risk_level": self.risk_level,
            "human_confirmation_required": self.human_confirmation_required,
            "blocked_actions": self.blocked_actions,
            "steps": [step.to_dict() for step in self.steps],
            "current_step_number": self.current_step_number,
            "confirmed_by": self.confirmed_by,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
