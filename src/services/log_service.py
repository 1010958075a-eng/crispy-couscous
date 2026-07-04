"""
产品B v0.9 - 日志中心服务
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.log import (
    Log,
    LogType,
    LogLevel,
    LogStatus
)
from .knowledge_storage import KnowledgeStorage


class LogService:
    """日志中心服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
    
    def create_log(
        self,
        log_type: str,
        source_module: str,
        source_id: Optional[str],
        action: str,
        status: str,
        message: str,
        risk_level: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ) -> Log:
        """创建日志记录"""
        log = Log(
            log_id=str(uuid.uuid4()),
            log_type=log_type,
            source_module=source_module,
            source_id=source_id,
            action=action,
            status=status,
            risk_level=risk_level,
            message=message,
            details=details
        )
        
        self.knowledge_storage.save_log(log)
        return log
    
    def get_logs(self) -> List[Dict[str, Any]]:
        """获取所有日志"""
        log_dicts = self.knowledge_storage.load_logs()
        return log_dicts if log_dicts else []
    
    def get_log(self, log_id: str) -> Optional[Dict[str, Any]]:
        """获取指定日志"""
        logs = self.get_logs()
        for log in logs:
            if log["log_id"] == log_id:
                return log
        return None
    
    def get_logs_by_type(self, log_type: str) -> List[Dict[str, Any]]:
        """按类型获取日志"""
        logs = self.get_logs()
        return [log for log in logs if log["log_type"] == log_type]
    
    def get_logs_by_source(self, source_module: str, source_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """按来源获取日志"""
        logs = self.get_logs()
        if source_id:
            return [log for log in logs if log["source_module"] == source_module and log["source_id"] == source_id]
        else:
            return [log for log in logs if log["source_module"] == source_module]
