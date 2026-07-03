"""
产品B v0.6 - 验收中心数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class AcceptanceStatus(str, Enum):
    """验收状态"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    REQUIRES_REVIEW = "requires_review"


class RiskLevel(str, Enum):
    """风险等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TargetType(str, Enum):
    """验收对象类型"""
    TASK = "task"
    LISTING_PACKAGE = "listing_package"
    DETAIL_SCREEN = "detail_screen"
    VIDEO_SCRIPT = "video_script"
    XIAOHONGSHU_NOTE = "xiaohongshu_note"


@dataclass
class AcceptanceIssue:
    """验收问题"""
    severity: str  # P0, P1, P2
    field: str
    issue: str
    suggestion: Optional[str] = None


@dataclass
class AcceptanceReport:
    """验收报告"""
    report_id: str
    target_type: str
    target_id: str
    status: str
    passed: bool
    p0_issues: List[AcceptanceIssue] = field(default_factory=list)
    p1_issues: List[AcceptanceIssue] = field(default_factory=list)
    p2_issues: List[AcceptanceIssue] = field(default_factory=list)
    risk_level: str = RiskLevel.LOW.value
    risk_items: List[str] = field(default_factory=list)
    human_confirmation_required: bool = False
    checked_fields: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)
    suggestions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "report_id": self.report_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "status": self.status,
            "passed": self.passed,
            "p0_issues": [self._issue_to_dict(issue) for issue in self.p0_issues],
            "p1_issues": [self._issue_to_dict(issue) for issue in self.p1_issues],
            "p2_issues": [self._issue_to_dict(issue) for issue in self.p2_issues],
            "risk_level": self.risk_level,
            "risk_items": self.risk_items,
            "human_confirmation_required": self.human_confirmation_required,
            "checked_fields": self.checked_fields,
            "missing_fields": self.missing_fields,
            "suggestions": self.suggestions,
            "created_at": self.created_at.isoformat()
        }

    def _issue_to_dict(self, issue: AcceptanceIssue):
        """问题转换为字典"""
        return {
            "severity": issue.severity,
            "field": issue.field,
            "issue": issue.issue,
            "suggestion": issue.suggestion
        }


# 合法的任务状态列表
VALID_TASK_STATUSES = [
    "pending",
    "planning",
    "in_progress",
    "waiting_confirmation",
    "completed",
    "failed",
    "cancelled"
]

# 高风险动作关键词
HIGH_RISK_KEYWORDS = [
    "自动登录",
    "自动上架",
    "自动改价",
    "自动开车",
    "自动投放",
    "自动改预算",
    "自动扣费",
    "保存账号密码",
    "auto.*login",
    "auto.*list",
    "auto.*price",
    "auto.*ad",
    "auto.*budget",
    "auto.*deduct"
]
