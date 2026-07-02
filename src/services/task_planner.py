"""
产品B - 一句话任务拆解服务
"""

import re
from typing import List, Dict, Any, Optional
from enum import Enum


class TaskType(str, Enum):
    """任务类型"""
    LINK_LEARNING = "link_learning"
    PRODUCT_GENERATION = "product_generation"
    COMPETITOR_ANALYSIS = "competitor_analysis"
    DATA_ANALYSIS = "data_analysis"
    OPTIMIZATION = "optimization"
    UNKNOWN = "unknown"


class TaskStep:
    """任务步骤"""
    def __init__(
        self,
        step_number: int,
        action: str,
        description: str,
        requires_confirmation: bool = False,
        risk_level: str = "low"
    ):
        self.step_number = step_number
        self.action = action
        self.description = description
        self.requires_confirmation = requires_confirmation
        self.risk_level = risk_level  # low, medium, high

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "step_number": self.step_number,
            "action": self.action,
            "description": self.description,
            "requires_confirmation": self.requires_confirmation,
            "risk_level": self.risk_level
        }


class TaskPlan:
    """任务计划"""
    def __init__(
        self,
        task_id: str,
        original_input: str,
        task_type: TaskType,
        steps: List[TaskStep]
    ):
        self.task_id = task_id
        self.original_input = original_input
        self.task_type = task_type
        self.steps = steps

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "task_id": self.task_id,
            "original_input": self.original_input,
            "task_type": self.task_type.value,
            "steps": [step.to_dict() for step in self.steps]
        }


class TaskPlanner:
    """任务规划器"""

    def __init__(self):
        """初始化任务规划器"""
        pass

    def parse_task(self, user_input: str) -> TaskPlan:
        """
        解析用户输入，生成任务计划

        Args:
            user_input: 用户输入的一句话任务

        Returns:
            任务计划
        """
        task_id = self._generate_task_id()
        task_type = self._identify_task_type(user_input)
        steps = self._generate_steps(user_input, task_type)

        return TaskPlan(
            task_id=task_id,
            original_input=user_input,
            task_type=task_type,
            steps=steps
        )

    def _generate_task_id(self) -> str:
        """生成任务ID"""
        import uuid
        return str(uuid.uuid4())

    def _identify_task_type(self, user_input: str) -> TaskType:
        """识别任务类型"""
        user_input_lower = user_input.lower()

        # 链接学习
        if any(keyword in user_input_lower for keyword in ["学习链接", "学习竞品", "链接学习", "抓取链接"]):
            return TaskType.LINK_LEARNING

        # 产品生成
        if any(keyword in user_input_lower for keyword in ["生成上架", "上架方案", "生成产品", "上架包", "生成标题", "生成详情"]):
            return TaskType.PRODUCT_GENERATION

        # 竞品分析
        if any(keyword in user_input_lower for keyword in ["竞品分析", "分析竞品", "竞品对比"]):
            return TaskType.COMPETITOR_ANALYSIS

        # 数据分析
        if any(keyword in user_input_lower for keyword in ["数据分析", "分析数据", "数据诊断", "查看数据"]):
            return TaskType.DATA_ANALYSIS

        # 优化
        if any(keyword in user_input_lower for keyword in ["优化", "提升", "改进", "建议"]):
            return TaskType.OPTIMIZATION

        return TaskType.UNKNOWN

    def _generate_steps(self, user_input: str, task_type: TaskType) -> List[TaskStep]:
        """根据任务类型生成步骤"""
        steps = []

        if task_type == TaskType.LINK_LEARNING:
            steps = self._generate_link_learning_steps(user_input)
        elif task_type == TaskType.PRODUCT_GENERATION:
            steps = self._generate_product_generation_steps(user_input)
        elif task_type == TaskType.COMPETITOR_ANALYSIS:
            steps = self._generate_competitor_analysis_steps(user_input)
        elif task_type == TaskType.DATA_ANALYSIS:
            steps = self._generate_data_analysis_steps(user_input)
        elif task_type == TaskType.OPTIMIZATION:
            steps = self._generate_optimization_steps(user_input)
        else:
            steps = self._generate_unknown_task_steps(user_input)

        return steps

    def _generate_link_learning_steps(self, user_input: str) -> List[TaskStep]:
        """生成链接学习步骤"""
        steps = [
            TaskStep(1, "extract_url", "从输入中提取链接URL", False, "low"),
            TaskStep(2, "fetch_content", "尝试读取链接内容", False, "low"),
            TaskStep(3, "manual_input", "如果自动抓取失败，提示用户手动输入内容", False, "low"),
            TaskStep(4, "extract_info", "提取标题、卖点、关键词", False, "low"),
            TaskStep(5, "save_knowledge", "保存到知识库", False, "low")
        ]
        return steps

    def _generate_product_generation_steps(self, user_input: str) -> List[TaskStep]:
        """生成产品生成步骤"""
        # 检查是否包含链接学习
        has_link = any(keyword in user_input for keyword in ["链接", "竞品", "学习"])
        product_name = self._extract_product_name(user_input)

        steps = []

        if has_link:
            steps.extend([
                TaskStep(1, "extract_url", "提取竞品链接", False, "low"),
                TaskStep(2, "learn_competitor", "学习竞品信息（标题、卖点、关键词）", False, "low"),
                TaskStep(3, "save_knowledge", "保存竞品知识到知识库", False, "low")
            ])

        steps.extend([
            TaskStep(len(steps) + 1, "generate_title", f"生成{product_name}的标题", False, "low"),
            TaskStep(len(steps) + 2, "generate_keywords", f"生成{product_name}的关键词", False, "low"),
            TaskStep(len(steps) + 3, "generate_image_prompts", "生成主图九宫格提示词", False, "low"),
            TaskStep(len(steps) + 4, "generate_detail_page", "生成详情页9屏内容", False, "low"),
            TaskStep(len(steps) + 5, "create_package", "生成待确认上架包", True, "low")  # 需要确认
        ])

        return steps

    def _generate_competitor_analysis_steps(self, user_input: str) -> List[TaskStep]:
        """生成竞品分析步骤"""
        steps = [
            TaskStep(1, "extract_competitor_info", "提取竞品信息", False, "low"),
            TaskStep(2, "analyze_price", "分析价格策略", False, "low"),
            TaskStep(3, "analyze_keywords", "分析关键词布局", False, "low"),
            TaskStep(4, "analyze_visual", "分析视觉风格", False, "low"),
            TaskStep(5, "generate_report", "生成竞品分析报告", True, "low")
        ]
        return steps

    def _generate_data_analysis_steps(self, user_input: str) -> List[TaskStep]:
        """生成数据分析步骤"""
        steps = [
            TaskStep(1, "load_data", "加载销售数据", False, "low"),
            TaskStep(2, "calculate_metrics", "计算关键指标（曝光、点击率、转化率、ROI）", False, "low"),
            TaskStep(3, "identify_trends", "识别数据趋势", False, "low"),
            TaskStep(4, "find_abnormal", "发现异常指标", False, "low"),
            TaskStep(5, "generate_suggestions", "生成优化建议", True, "low")
        ]
        return steps

    def _generate_optimization_steps(self, user_input: str) -> List[TaskStep]:
        """生成优化步骤"""
        steps = [
            TaskStep(1, "analyze_current", "分析当前状态", False, "low"),
            TaskStep(2, "identify_issues", "识别问题点", False, "low"),
            TaskStep(3, "generate_solutions", "生成解决方案", False, "low"),
            TaskStep(4, "estimate_impact", "预估优化效果", False, "low"),
            TaskStep(5, "create_action_plan", "创建待确认执行计划", True, "medium")
        ]
        return steps

    def _generate_unknown_task_steps(self, user_input: str) -> List[TaskStep]:
        """生成未知任务步骤"""
        steps = [
            TaskStep(1, "analyze_intent", "分析用户意图", False, "low"),
            TaskStep(2, "clarify_requirements", "明确具体需求", False, "low"),
            TaskStep(3, "suggest_approach", "建议处理方案", False, "low")
        ]
        return steps

    def _extract_product_name(self, user_input: str) -> str:
        """从输入中提取产品名称"""
        # 简化版本：尝试提取"生成一款XXX"或"生成XXX"中的产品名
        patterns = [
            r'生成一款(.+?)的',
            r'生成(.+?)的',
            r'同类(.+?)的',
            r'一款(.+?)的'
        ]

        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                return match.group(1).strip()

        return "产品"

    def execute_step(self, step: TaskStep, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        执行单个步骤（简化版本，只返回待执行状态）

        Args:
            step: 任务步骤
            context: 上下文信息

        Returns:
            执行结果
        """
        # 简化版本：只返回步骤信息，不实际执行
        return {
            "step": step.to_dict(),
            "status": "pending",
            "message": f"步骤 {step.step_number} 待执行：{step.description}",
            "requires_confirmation": step.requires_confirmation
        }
