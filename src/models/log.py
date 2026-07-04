"""
产品B v0.9 - 日志中心数据模型
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum


class LogType(str, Enum):
    """日志类型"""
    TASK = "task"
    TOOL = "tool"
    ACCEPTANCE = "acceptance"
    WORKFLOW = "workflow"
    RISK = "risk"
    SYSTEM = "system"


class LogLevel(str, Enum):
    """日志级别"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogStatus(str, Enum):
    """日志状态"""
    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"
    BLOCKED = "blocked"


@dataclass
class Log:
    """日志记录"""
    log_id: str
    log_type: str
    source_module: str
    source_id: Optional[str]
    action: str
    status: str
    risk_level: Optional[str]
    message: str
    details: Optional[Dict[str, Any]]
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        """转换为字典"""
        return {
            "log_id": self.log_id,
            "log_type": self.log_type,
            "source_module": self.source_module,
            "source_id": self.source_id,
            "action": self.action,
            "status": self.status,
            "risk_level": self.risk_level,
            "message": self.message,
            "details": self.details,
            "created_at": self.created_at.isoformat()
        }
