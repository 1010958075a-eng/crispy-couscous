"""
产品B v0.8 - 工作流中心服务
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.workflow import (
    Workflow,
    WorkflowStep,
    WorkflowStatus,
    StepStatus,
    StepType
)
from models.tool import RiskLevel
from .knowledge_storage import KnowledgeStorage
from .task_service import TaskService
from .tool_service import ToolService


# 高风险动作关键词
HIGH_RISK_KEYWORDS = [
    "自动登录",
    "自动上架",
    "自动改价",
    "自动开车",
    "开车投放",
    "自动投放",
    "自动改预算",
    "自动扣费",
    "保存账号密码"
]


class WorkflowService:
    """工作流中心服务"""
    
    def __init__(
        self,
        knowledge_storage: KnowledgeStorage,
        task_service: TaskService,
        tool_service: ToolService
    ):
        self.knowledge_storage = knowledge_storage
        self.task_service = task_service
        self.tool_service = tool_service
    
    def create_workflow(self, original_request: str) -> Workflow:
        """创建工作流"""
        
        # 扫描高风险关键词
        blocked_actions = []
        for keyword in HIGH_RISK_KEYWORDS:
            if keyword in original_request:
                # 将"开车投放"转换为"自动开车"和"自动投放"
                if keyword == "开车投放":
                    blocked_actions.append("自动开车")
                    blocked_actions.append("自动投放")
                else:
                    blocked_actions.append(keyword)
        
        # 去重
        blocked_actions = list(set(blocked_actions))
        
        # 确定风险级别
        if blocked_actions:
            risk_level = RiskLevel.HIGH.value
            human_confirmation_required = True
            workflow_status = WorkflowStatus.BLOCKED.value
        else:
            risk_level = RiskLevel.LOW.value
            human_confirmation_required = False
            workflow_status = WorkflowStatus.PENDING.value
        
        # 创建任务（复用任务中心）
        task = self.task_service.create_task(
            original_request=original_request,
            priority="medium"
        )
        task_id = task.task_id if task else None
        
        # 推荐工具（复用工具中心）
        recommended_tools = self.tool_service.suggest_tools(original_request)
        
        # 生成工具计划（复用工具中心）
        tool_plan = self.tool_service.generate_tool_plan(original_request, task_id)
        
        # 创建工作流步骤
        steps = self._create_workflow_steps(
            task_id=task_id,
            recommended_tools=recommended_tools,
            tool_plan=tool_plan,
            blocked_actions=blocked_actions
        )
        
        workflow = Workflow(
            workflow_id=str(uuid.uuid4()),
            original_request=original_request,
            task_id=task_id,
            workflow_status=workflow_status,
            risk_level=risk_level,
            human_confirmation_required=human_confirmation_required,
            blocked_actions=blocked_actions,
            steps=steps,
            current_step_number=1
        )
        
        # 保存工作流
        self.knowledge_storage.save_workflow(workflow)
        
        return workflow
    
    def _create_workflow_steps(
        self,
        task_id: Optional[str],
        recommended_tools: List[Dict[str, Any]],
        tool_plan: Any,
        blocked_actions: List[str]
    ) -> List[WorkflowStep]:
        """创建工作流步骤"""
        steps = []
        step_number = 1
        
        # 步骤1: 创建任务
        steps.append(WorkflowStep(
            step_number=step_number,
            step_name="创建任务",
            step_type=StepType.TASK_CREATION.value,
            description="在任务中心创建任务记录",
            status=StepStatus.COMPLETED.value,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            result={"task_id": task_id}
        ))
        step_number += 1
        
        # 步骤2: 推荐工具
        steps.append(WorkflowStep(
            step_number=step_number,
            step_name="推荐工具",
            step_type=StepType.TOOL_RECOMMENDATION.value,
            description="根据任务需求推荐工具",
            status=StepStatus.COMPLETED.value,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            result={"recommended_tools": [t.get("tool_id") for t in recommended_tools]}
        ))
        step_number += 1
        
        # 步骤3: 生成工具计划
        steps.append(WorkflowStep(
            step_number=step_number,
            step_name="生成工具计划",
            step_type=StepType.TOOL_PLAN_GENERATION.value,
            description="生成工具调用计划",
            status=StepStatus.COMPLETED.value,
            started_at=datetime.now(),
            completed_at=datetime.now(),
            result={"tool_plan_id": tool_plan.plan_id if tool_plan else None}
        ))
        step_number += 1
        
        # 步骤4: 内容生成（占位）
        if not blocked_actions:
            steps.append(WorkflowStep(
                step_number=step_number,
                step_name="内容生成",
                step_type=StepType.CONTENT_GENERATION.value,
                description="生成内容（占位，本阶段不执行）",
                status=StepStatus.PENDING.value,
                result={"message": "本阶段为占位，不实际执行内容生成"}
            ))
            step_number += 1
        
        # 步骤5: 验收检查
        if not blocked_actions:
            steps.append(WorkflowStep(
                step_number=step_number,
                step_name="验收检查",
                step_type=StepType.ACCEPTANCE_CHECK.value,
                description="检查生成内容完整性",
                status=StepStatus.PENDING.value,
                result={"message": "等待执行"}
            ))
            step_number += 1
        
        # 步骤6: 风险检查
        if blocked_actions:
            steps.append(WorkflowStep(
                step_number=step_number,
                step_name="风险检查",
                step_type=StepType.RISK_CHECK.value,
                description="检查高风险动作",
                status=StepStatus.COMPLETED.value,
                started_at=datetime.now(),
                completed_at=datetime.now(),
                result={"blocked_actions": blocked_actions}
            ))
            step_number += 1
        
        # 步骤7: 人工确认（仅高风险）
        if blocked_actions:
            steps.append(WorkflowStep(
                step_number=step_number,
                step_name="人工确认",
                step_type=StepType.MANUAL_CONFIRMATION.value,
                description="高风险动作需要人工确认",
                status=StepStatus.PENDING.value,
                result={"message": "等待人工确认"}
            ))
            step_number += 1
        
        # 步骤8: 完成归档
        steps.append(WorkflowStep(
            step_number=step_number,
            step_name="完成归档",
            step_type=StepType.ARCHIVE.value,
            description="工作流完成归档",
            status=StepStatus.PENDING.value,
            result={"message": "等待完成"}
        ))
        
        return steps
    
    def get_workflows(self) -> List[Dict[str, Any]]:
        """获取所有工作流"""
        workflow_dicts = self.knowledge_storage.load_workflows()
        return workflow_dicts if workflow_dicts else []
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """获取指定工作流"""
        workflows = self.get_workflows()
        for workflow in workflows:
            if workflow["workflow_id"] == workflow_id:
                return workflow
        return None
    
    def update_workflow_status(
        self,
        workflow_id: str,
        status: str
    ) -> Optional[Dict[str, Any]]:
        """更新工作流状态"""
        workflow_dict = self.get_workflow(workflow_id)
        if not workflow_dict:
            return None
        
        workflow_dict["workflow_status"] = status
        workflow_dict["updated_at"] = datetime.now().isoformat()
        
        # 更新存储
        workflows = self.get_workflows()
        updated_workflows = []
        for wf in workflows:
            if wf["workflow_id"] == workflow_id:
                updated_workflows.append(workflow_dict)
            else:
                updated_workflows.append(wf)
        
        self.knowledge_storage.save_workflows(updated_workflows)
        
        return workflow_dict
    
    def update_step_status(
        self,
        workflow_id: str,
        step_number: int,
        status: str,
        result: Optional[Dict[str, Any]] = None,
        error_message: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """更新步骤状态"""
        workflow_dict = self.get_workflow(workflow_id)
        if not workflow_dict:
            return None
        
        # 更新指定步骤
        for step in workflow_dict["steps"]:
            if step["step_number"] == step_number:
                step["status"] = status
                if status == StepStatus.RUNNING.value:
                    step["started_at"] = datetime.now().isoformat()
                elif status == StepStatus.COMPLETED.value:
                    step["completed_at"] = datetime.now().isoformat()
                if result:
                    step["result"] = result
                if error_message:
                    step["error_message"] = error_message
                break
        
        workflow_dict["updated_at"] = datetime.now().isoformat()
        
        # 更新存储
        workflows = self.get_workflows()
        updated_workflows = []
        for wf in workflows:
            if wf["workflow_id"] == workflow_id:
                updated_workflows.append(workflow_dict)
            else:
                updated_workflows.append(wf)
        
        self.knowledge_storage.save_workflows(updated_workflows)
        
        return workflow_dict
    
    def confirm_workflow(
        self,
        workflow_id: str,
        confirmed_by: str
    ) -> Optional[Dict[str, Any]]:
        """确认工作流（人工确认）"""
        workflow_dict = self.get_workflow(workflow_id)
        if not workflow_dict:
            return None
        
        # 检查是否需要人工确认
        if not workflow_dict["human_confirmation_required"]:
            return None
        
        # 更新确认信息
        workflow_dict["confirmed_by"] = confirmed_by
        workflow_dict["confirmed_at"] = datetime.now().isoformat()
        workflow_dict["workflow_status"] = WorkflowStatus.RUNNING.value
        workflow_dict["updated_at"] = datetime.now().isoformat()
        
        # 更新人工确认步骤状态
        for step in workflow_dict["steps"]:
            if step["step_type"] == StepType.MANUAL_CONFIRMATION.value:
                step["status"] = StepStatus.COMPLETED.value
                step["completed_at"] = datetime.now().isoformat()
                step["result"] = {"confirmed_by": confirmed_by}
                break
        
        # 更新存储
        workflows = self.get_workflows()
        updated_workflows = []
        for wf in workflows:
            if wf["workflow_id"] == workflow_id:
                updated_workflows.append(workflow_dict)
            else:
                updated_workflows.append(wf)
        
        self.knowledge_storage.save_workflows(updated_workflows)
        
        return workflow_dict
