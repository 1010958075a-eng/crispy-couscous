"""
产品B v0.6 - 验收中心服务
"""

import uuid
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.acceptance import (
    AcceptanceReport,
    AcceptanceIssue,
    RiskLevel,
    TargetType,
    VALID_TASK_STATUSES,
    HIGH_RISK_KEYWORDS
)
from .knowledge_storage import KnowledgeStorage


class AcceptanceService:
    """验收中心服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
    
    def check_task(self, task_data: Dict[str, Any]) -> AcceptanceReport:
        """检查任务记录是否合规"""
        report = AcceptanceReport(
            report_id=str(uuid.uuid4()),
            target_type=TargetType.TASK.value,
            target_id=task_data.get("task_id", ""),
            status="in_progress",
            passed=False
        )
        
        # 检查必需字段
        required_fields = [
            "task_id",
            "task_title",
            "original_request",
            "task_type",
            "status",
            "priority"
        ]
        
        for field in required_fields:
            if field not in task_data or not task_data[field]:
                report.missing_fields.append(field)
                report.p0_issues.append(AcceptanceIssue(
                    severity="P0",
                    field=field,
                    issue=f"缺少必需字段: {field}",
                    suggestion=f"请提供 {field} 字段"
                ))
        
        # 检查任务状态合法性
        status = task_data.get("status")
        if status and status not in VALID_TASK_STATUSES:
            report.p0_issues.append(AcceptanceIssue(
                severity="P0",
                field="status",
                issue=f"非法任务状态: {status}",
                suggestion=f"任务状态必须是: {', '.join(VALID_TASK_STATUSES)}"
            ))
        
        # 检查步骤字段
        steps = task_data.get("steps", [])
        if not steps:
            report.p1_issues.append(AcceptanceIssue(
                severity="P1",
                field="steps",
                issue="任务缺少步骤",
                suggestion="请添加任务步骤"
            ))
        else:
            for step in steps:
                step_required = [
                    "step_number",
                    "step_name",
                    "step_description",
                    "related_module",
                    "status",
                    "requires_human_confirmation",
                    "risk_level",
                    "expected_output"
                ]
                for field in step_required:
                    if field not in step:
                        report.p2_issues.append(AcceptanceIssue(
                            severity="P2",
                            field=f"steps.{field}",
                            issue=f"步骤缺少字段: {field}"
                        ))
        
        # 检查高风险动作
        task_text = str(task_data)
        for keyword in HIGH_RISK_KEYWORDS:
            if re.search(keyword, task_text, re.IGNORECASE):
                report.risk_items.append(keyword)
        
        if report.risk_items:
            report.risk_level = RiskLevel.HIGH.value
            report.human_confirmation_required = True
            report.suggestions.append("检测到高风险动作，需要人工确认")
        else:
            report.risk_level = RiskLevel.LOW.value
        
        # 检查人工确认要求
        if task_data.get("human_confirmation_required"):
            report.human_confirmation_required = True
        
        # 更新报告状态
        if not report.p0_issues and not report.p1_issues:
            report.passed = True
            report.status = "passed"
        elif report.p0_issues:
            report.status = "failed"
        else:
            report.status = "requires_review"
        
        return report
    
    def check_package(self, package_data: Dict[str, Any]) -> AcceptanceReport:
        """检查上架包是否字段完整"""
        report = AcceptanceReport(
            report_id=str(uuid.uuid4()),
            target_type=TargetType.LISTING_PACKAGE.value,
            target_id=package_data.get("package_id", ""),
            status="in_progress",
            passed=False
        )
        
        # 检查必需字段
        required_fields = [
            "package_id",
            "product_id",
            "titles",
            "keywords",
            "image_prompts"
        ]
        
        for field in required_fields:
            if field not in package_data or not package_data[field]:
                report.missing_fields.append(field)
                report.p0_issues.append(AcceptanceIssue(
                    severity="P0",
                    field=field,
                    issue=f"缺少必需字段: {field}",
                    suggestion=f"请提供 {field} 字段"
                ))
        
        # 检查标题数量
        titles = package_data.get("titles", [])
        if len(titles) < 10:
            report.p1_issues.append(AcceptanceIssue(
                severity="P1",
                field="titles",
                issue=f"标题数量不足: {len(titles)}",
                suggestion="建议至少生成10个标题"
            ))
        
        # 检查关键词
        keywords = package_data.get("keywords", [])
        if not keywords:
            report.p1_issues.append(AcceptanceIssue(
                severity="P1",
                field="keywords",
                issue="缺少关键词",
                suggestion="请提供关键词"
            ))
        
        # 检查高风险动作
        package_text = str(package_data)
        for keyword in HIGH_RISK_KEYWORDS:
            if re.search(keyword, package_text, re.IGNORECASE):
                report.risk_items.append(keyword)
        
        if report.risk_items:
            report.risk_level = RiskLevel.HIGH.value
            report.human_confirmation_required = True
        else:
            report.risk_level = RiskLevel.LOW.value
        
        # 更新报告状态
        if not report.p0_issues and not report.p1_issues:
            report.passed = True
            report.status = "passed"
        elif report.p0_issues:
            report.status = "failed"
        else:
            report.status = "requires_review"
        
        return report
    
    def check_risk(self, text: str) -> Dict[str, Any]:
        """检查文本或任务内容是否包含高风险动作"""
        risk_items = []
        
        for keyword in HIGH_RISK_KEYWORDS:
            if re.search(keyword, text, re.IGNORECASE):
                risk_items.append(keyword)
        
        return {
            "has_risk": len(risk_items) > 0,
            "risk_items": risk_items,
            "risk_level": RiskLevel.HIGH.value if risk_items else RiskLevel.LOW.value,
            "human_confirmation_required": len(risk_items) > 0
        }
    
    def validate_task_status(self, status: str) -> bool:
        """验证任务状态是否合法"""
        return status in VALID_TASK_STATUSES
