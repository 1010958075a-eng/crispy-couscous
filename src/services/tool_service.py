"""
产品B v0.7 - 工具中心服务
"""

import uuid
import re
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.tool import (
    Tool,
    ToolPlan,
    ExecutionStep,
    BUILTIN_TOOLS,
    RiskLevel,
    PlanStatus
)
from .knowledge_storage import KnowledgeStorage


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


class ToolService:
    """工具中心服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
        self._initialize_tool_registry()
        self.tools = self._load_tools()
    
    def _initialize_tool_registry(self):
        """初始化工具注册表"""
        # 检查工具注册表是否存在
        existing_tools = self.knowledge_storage.load_tool_registry()
        if not existing_tools:
            # 如果不存在，创建并保存内置工具
            self.knowledge_storage.save_tool_registry(BUILTIN_TOOLS)
    
    def _load_tools(self) -> List[Tool]:
        """从存储加载工具"""
        tool_dicts = self.knowledge_storage.load_tool_registry()
        if tool_dicts:
            # 从存储恢复工具对象
            tools = []
            for tool_dict in tool_dicts:
                tool = Tool(
                    tool_id=tool_dict["tool_id"],
                    tool_name=tool_dict["tool_name"],
                    tool_category=tool_dict["tool_category"],
                    tool_type=tool_dict["tool_type"],
                    description=tool_dict["description"],
                    related_module=tool_dict["related_module"],
                    related_api=tool_dict["related_api"],
                    input_requirements=tool_dict["input_requirements"],
                    output_description=tool_dict["output_description"],
                    risk_level=tool_dict["risk_level"],
                    requires_human_confirmation=tool_dict["requires_human_confirmation"],
                    enabled=tool_dict["enabled"]
                )
                tools.append(tool)
            return tools
        else:
            # 如果存储为空，使用内置工具
            return BUILTIN_TOOLS
    
    def get_tools(self) -> List[Dict[str, Any]]:
        """获取所有工具"""
        return [tool.to_dict() for tool in self.tools]
    
    def get_tool(self, tool_id: str) -> Optional[Dict[str, Any]]:
        """获取指定工具"""
        for tool in self.tools:
            if tool.tool_id == tool_id:
                return tool.to_dict()
        return None
    
    def suggest_tools(self, request: str) -> List[Dict[str, Any]]:
        """根据一句话任务推荐工具"""
        request_lower = request.lower()
        recommended = []
        
        # 规则匹配推荐
        if "标题" in request:
            recommended.append(self.get_tool("title_generator"))
        if "关键词" in request:
            recommended.append(self.get_tool("keyword_generator"))
        if "主图" in request or "提示词" in request:
            recommended.append(self.get_tool("main_image_prompt_generator"))
        if "上架" in request or "包" in request:
            recommended.append(self.get_tool("listing_package_generator"))
        if "详情页" in request:
            recommended.append(self.get_tool("detail_screen_generator"))
        if "视频" in request or "脚本" in request:
            recommended.append(self.get_tool("video_script_generator"))
        if "小红书" in request:
            recommended.append(self.get_tool("xiaohongshu_generator"))
        
        # 如果没有匹配到，推荐通用上架包生成器
        if not recommended:
            recommended.append(self.get_tool("listing_package_generator"))
        
        # 去除None值
        recommended = [tool for tool in recommended if tool is not None]
        
        return recommended
    
    def suggest_tools_for_task(self, task_id: str) -> List[Dict[str, Any]]:
        """根据task_id推荐工具"""
        # 读取任务信息
        task = self.knowledge_storage.load_task(task_id)
        if not task:
            return []
        
        # 根据任务类型推荐工具
        task_type = task.get("task_type", "")
        original_request = task.get("original_request", "")
        
        # 先根据原始请求推荐
        recommended = self.suggest_tools(original_request)
        
        # 添加任务中心工具
        if "task_center" not in [tool.get("tool_id") for tool in recommended]:
            recommended.append(self.get_tool("task_center"))
        
        # 添加验收检查器
        if "acceptance_checker" not in [tool.get("tool_id") for tool in recommended]:
            recommended.append(self.get_tool("acceptance_checker"))
        
        # 去除None值
        recommended = [tool for tool in recommended if tool is not None]
        
        return recommended
    
    def generate_tool_plan(
        self,
        original_request: str,
        task_id: Optional[str] = None
    ) -> ToolPlan:
        """生成工具调用计划"""
        
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
        
        # 如果检测到高风险动作
        if blocked_actions:
            risk_level = RiskLevel.HIGH.value
            human_confirmation_required = True
            plan_status = PlanStatus.BLOCKED.value
        else:
            risk_level = RiskLevel.LOW.value
            human_confirmation_required = False
            plan_status = PlanStatus.PENDING.value
        
        # 推荐工具
        if task_id:
            recommended_tools = self.suggest_tools_for_task(task_id)
        else:
            recommended_tools = self.suggest_tools(original_request)
        
        # 生成执行步骤
        execution_steps = []
        step_number = 1
        
        for tool_dict in recommended_tools:
            step = ExecutionStep(
                step_number=step_number,
                step_name=f"使用 {tool_dict['tool_name']}",
                tool_id=tool_dict['tool_id'],
                tool_name=tool_dict['tool_name'],
                reason=f"根据任务需求推荐",
                expected_output=tool_dict['output_description'],
                risk_level=tool_dict['risk_level'],
                requires_human_confirmation=tool_dict['requires_human_confirmation']
            )
            execution_steps.append(step)
            step_number += 1
        
        # 添加验收步骤（仅在非高风险情况下）
        if not blocked_actions:
            acceptance_step = ExecutionStep(
                step_number=step_number,
                step_name="验收检查",
                tool_id="acceptance_checker",
                tool_name="验收检查器",
                reason="检查生成内容完整性",
                expected_output="验收报告",
                risk_level=RiskLevel.MEDIUM.value,
                requires_human_confirmation=False
            )
            execution_steps.append(acceptance_step)
            step_number += 1
        
        # 添加风险检查步骤
        if blocked_actions:
            risk_step = ExecutionStep(
                step_number=step_number,
                step_name="风险检查",
                tool_id="risk_checker",
                tool_name="风险检查器",
                reason="检查高风险动作",
                expected_output="风险识别结果",
                risk_level=RiskLevel.MEDIUM.value,
                requires_human_confirmation=False
            )
            execution_steps.append(risk_step)
        
        plan = ToolPlan(
            plan_id=str(uuid.uuid4()),
            original_request=original_request,
            task_id=task_id,
            recommended_tools=[tool.get("tool_id") for tool in recommended_tools],
            execution_steps=execution_steps,
            risk_level=risk_level,
            human_confirmation_required=human_confirmation_required,
            blocked_actions=blocked_actions,
            plan_status=plan_status
        )
        
        return plan
