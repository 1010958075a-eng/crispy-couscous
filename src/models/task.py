"""
产品B v0.5 - Agent任务中心数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class TaskStatus(str, Enum):
    """任务状态"""
    PENDING = "pending"
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    WAITING_CONFIRMATION = "waiting_confirmation"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class RiskLevel(str, Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class TaskStep:
    """任务步骤"""
    step_number: int
    step_name: str
    step_description: str
    related_module: str
    status: str
    requires_human_confirmation: bool
    risk_level: str
    expected_output: str
    completed_at: Optional[datetime] = None
    notes: Optional[str] = None


@dataclass
class Task:
    """任务主记录"""
    task_id: str
    task_title: str
    original_request: str
    task_type: str
    product_id: Optional[str]
    related_package_id: Optional[str]
    status: str
    priority: str
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    steps: List[TaskStep] = field(default_factory=list)
    human_confirmation_required: bool = False
    risk_notes: Optional[str] = None
    final_summary: Optional[str] = None

    def to_dict(self):
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "task_title": self.task_title,
            "original_request": self.original_request,
            "task_type": self.task_type,
            "product_id": self.product_id,
            "related_package_id": self.related_package_id,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "steps": [self._step_to_dict(step) for step in self.steps],
            "human_confirmation_required": self.human_confirmation_required,
            "risk_notes": self.risk_notes,
            "final_summary": self.final_summary
        }

    def _step_to_dict(self, step: TaskStep):
        """步骤转换为字典"""
        return {
            "step_number": step.step_number,
            "step_name": step.step_name,
            "step_description": step.step_description,
            "related_module": step.related_module,
            "status": step.status,
            "requires_human_confirmation": step.requires_human_confirmation,
            "risk_level": step.risk_level,
            "expected_output": step.expected_output,
            "completed_at": step.completed_at.isoformat() if step.completed_at else None,
            "notes": step.notes
        }
