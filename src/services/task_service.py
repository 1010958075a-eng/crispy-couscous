"""
产品B v0.5 - Agent任务中心服务
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.task import Task, TaskStep, TaskStatus, RiskLevel
from models.acceptance import VALID_TASK_STATUSES
from .knowledge_storage import KnowledgeStorage


class TaskService:
    """任务中心服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
    
    def create_task(
        self,
        original_request: str,
        product_id: Optional[str] = None,
        related_package_id: Optional[str] = None,
        priority: str = "medium"
    ) -> Task:
        """创建任务并自动拆解步骤"""
        
        # 分析任务类型
        task_type = self._analyze_task_type(original_request)
        
        # 生成任务标题
        task_title = self._generate_task_title(original_request)
        
        # 拆解任务步骤
        steps = self._decompose_task(
            original_request=original_request,
            task_type=task_type,
            product_id=product_id
        )
        
        # 检查是否需要人工确认
        human_confirmation_required = any(
            step.requires_human_confirmation for step in steps
        )
        
        # 生成风险说明
        risk_notes = self._generate_risk_notes(steps)
        
        return Task(
            task_id=str(uuid.uuid4()),
            task_title=task_title,
            original_request=original_request,
            task_type=task_type,
            product_id=product_id,
            related_package_id=related_package_id,
            status=TaskStatus.PENDING.value,
            priority=priority,
            steps=steps,
            human_confirmation_required=human_confirmation_required,
            risk_notes=risk_notes
        )
    
    def _analyze_task_type(self, original_request: str) -> str:
        """分析任务类型"""
        request_lower = original_request.lower()
        
        if "上架" in original_request or "发布" in original_request:
            return "listing_package"
        elif "详情页" in original_request:
            return "detail_page"
        elif "短视频" in original_request or "视频" in original_request:
            return "video_script"
        elif "小红书" in original_request:
            return "xiaohongshu"
        elif "标题" in original_request:
            return "title_generation"
        elif "关键词" in original_request:
            return "keyword_generation"
        else:
            return "general"
    
    def _generate_task_title(self, original_request: str) -> str:
        """生成任务标题"""
        # 简单取前30个字符作为标题
        return original_request[:30] + ("..." if len(original_request) > 30 else "")
    
    def _decompose_task(
        self,
        original_request: str,
        task_type: str,
        product_id: Optional[str]
    ) -> List[TaskStep]:
        """拆解任务步骤"""
        
        steps = []
        
        if task_type == "listing_package":
            # 完整上架方案任务
            steps = self._decompose_listing_package_task(original_request, product_id)
        elif task_type == "detail_page":
            # 详情页生成任务
            steps = self._decompose_detail_page_task(original_request, product_id)
        elif task_type == "video_script":
            # 短视频脚本任务
            steps = self._decompose_video_script_task(original_request, product_id)
        elif task_type == "xiaohongshu":
            # 小红书文案任务
            steps = self._decompose_xiaohongshu_task(original_request, product_id)
        else:
            # 通用任务
            steps = self._decompose_general_task(original_request, product_id)
        
        return steps
    
    def _decompose_listing_package_task(
        self,
        original_request: str,
        product_id: Optional[str]
    ) -> List[TaskStep]:
        """拆解上架包任务"""
        steps = [
            TaskStep(
                step_number=1,
                step_name="读取商家档案",
                step_description="读取商家基础信息和运营偏好",
                related_module="knowledge_storage",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="商家档案信息"
            ),
            TaskStep(
                step_number=2,
                step_name="读取产品知识",
                step_description="读取产品相关信息和卖点",
                related_module="knowledge_storage",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="产品知识信息"
            ),
            TaskStep(
                step_number=3,
                step_name="生成20个标题",
                step_description="基于产品知识生成多个标题选项",
                related_module="title_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="20个标题列表"
            ),
            TaskStep(
                step_number=4,
                step_name="生成关键词包",
                step_description="生成核心关键词和长尾关键词",
                related_module="keyword_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="关键词包"
            ),
            TaskStep(
                step_number=5,
                step_name="生成主图九宫格提示词",
                step_description="生成主图设计提示词",
                related_module="image_prompt_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="9个主图提示词"
            ),
            TaskStep(
                step_number=6,
                step_name="生成详情页9屏",
                step_description="生成详情页9屏内容",
                related_module="detail_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="详情页9屏"
            ),
            TaskStep(
                step_number=7,
                step_name="生成短视频脚本",
                step_description="生成短视频拍摄脚本",
                related_module="content_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="短视频脚本"
            ),
            TaskStep(
                step_number=8,
                step_name="生成小红书文案",
                step_description="生成小红书种草文案",
                related_module="content_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="小红书文案"
            ),
            TaskStep(
                step_number=9,
                step_name="汇总上架方案",
                step_description="整合所有生成内容为完整方案",
                related_module="package_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="完整上架方案"
            ),
            TaskStep(
                step_number=10,
                step_name="等待人工确认",
                step_description="等待用户确认上架方案",
                related_module="human_confirmation",
                status="pending",
                requires_human_confirmation=True,
                risk_level=RiskLevel.LOW.value,
                expected_output="人工确认结果"
            )
        ]
        
        return steps
    
    def _decompose_detail_page_task(
        self,
        original_request: str,
        product_id: Optional[str]
    ) -> List[TaskStep]:
        """拆解详情页任务"""
        steps = [
            TaskStep(
                step_number=1,
                step_name="读取产品知识",
                step_description="读取产品相关信息",
                related_module="knowledge_storage",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="产品知识信息"
            ),
            TaskStep(
                step_number=2,
                step_name="生成详情页9屏",
                step_description="生成详情页9屏内容",
                related_module="detail_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="详情页9屏"
            ),
            TaskStep(
                step_number=3,
                step_name="等待人工确认",
                step_description="等待用户确认详情页内容",
                related_module="human_confirmation",
                status="pending",
                requires_human_confirmation=True,
                risk_level=RiskLevel.LOW.value,
                expected_output="人工确认结果"
            )
        ]
        
        return steps
    
    def _decompose_video_script_task(
        self,
        original_request: str,
        product_id: Optional[str]
    ) -> List[TaskStep]:
        """拆解短视频脚本任务"""
        steps = [
            TaskStep(
                step_number=1,
                step_name="读取产品知识",
                step_description="读取产品相关信息",
                related_module="knowledge_storage",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="产品知识信息"
            ),
            TaskStep(
                step_number=2,
                step_name="生成短视频脚本",
                step_description="生成短视频拍摄脚本",
                related_module="content_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="短视频脚本"
            ),
            TaskStep(
                step_number=3,
                step_name="等待人工确认",
                step_description="等待用户确认脚本内容",
                related_module="human_confirmation",
                status="pending",
                requires_human_confirmation=True,
                risk_level=RiskLevel.LOW.value,
                expected_output="人工确认结果"
            )
        ]
        
        return steps
    
    def _decompose_xiaohongshu_task(
        self,
        original_request: str,
        product_id: Optional[str]
    ) -> List[TaskStep]:
        """拆解小红书文案任务"""
        steps = [
            TaskStep(
                step_number=1,
                step_name="读取产品知识",
                step_description="读取产品相关信息",
                related_module="knowledge_storage",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="产品知识信息"
            ),
            TaskStep(
                step_number=2,
                step_name="生成小红书文案",
                step_description="生成小红书种草文案",
                related_module="content_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="小红书文案"
            ),
            TaskStep(
                step_number=3,
                step_name="等待人工确认",
                step_description="等待用户确认文案内容",
                related_module="human_confirmation",
                status="pending",
                requires_human_confirmation=True,
                risk_level=RiskLevel.LOW.value,
                expected_output="人工确认结果"
            )
        ]
        
        return steps
    
    def _decompose_general_task(
        self,
        original_request: str,
        product_id: Optional[str]
    ) -> List[TaskStep]:
        """拆解通用任务"""
        steps = [
            TaskStep(
                step_number=1,
                step_name="分析需求",
                step_description="分析用户需求",
                related_module="task_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="需求分析结果"
            ),
            TaskStep(
                step_number=2,
                step_name="执行任务",
                step_description="执行具体任务",
                related_module="task_service",
                status="pending",
                requires_human_confirmation=False,
                risk_level=RiskLevel.LOW.value,
                expected_output="任务执行结果"
            ),
            TaskStep(
                step_number=3,
                step_name="等待人工确认",
                step_description="等待用户确认结果",
                related_module="human_confirmation",
                status="pending",
                requires_human_confirmation=True,
                risk_level=RiskLevel.LOW.value,
                expected_output="人工确认结果"
            )
        ]
        
        return steps
    
    def _generate_risk_notes(self, steps: List[TaskStep]) -> str:
        """生成风险说明"""
        high_risk_steps = [s for s in steps if s.risk_level == RiskLevel.HIGH.value]
        if high_risk_steps:
            return f"包含{len(high_risk_steps)}个高风险步骤，需要人工确认"
        return "任务风险较低"
    
    def update_task_status(
        self,
        task_id: str,
        status: str
    ) -> Optional[Task]:
        """更新任务状态"""
        # 验证状态合法性
        if status not in VALID_TASK_STATUSES:
            raise ValueError(f"非法任务状态: {status}，合法状态: {VALID_TASK_STATUSES}")
        # 这里需要从存储中加载任务
        # 由于TaskService不直接管理存储，这个方法主要用于逻辑验证
        # 实际更新由API层调用knowledge_storage完成
        return None
    
    def validate_task_status(self, status: str) -> bool:
        """验证任务状态是否合法"""
        return status in VALID_TASK_STATUSES
