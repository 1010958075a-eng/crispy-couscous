"""
产品B v1.3 - 模型路由中心 / 业务层 MoE 雏形服务
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.model_router import (
    ModelProfile,
    BusinessExpert,
    ModelRouteRule,
    ModelRouteDecision,
    BUILTIN_MODEL_PROFILES,
    BUILTIN_BUSINESS_EXPERTS,
    BUILTIN_ROUTE_RULES,
    HIGH_RISK_FEATURES,
    RoutePolicy,
    TaskType,
    CostLevel,
    QualityLevel
)
from .knowledge_storage import KnowledgeStorage
from .api_provider_service import ApiProviderService
from .subscription_service import SubscriptionService


class ModelRouterService:
    """模型路由中心服务"""
    
    def __init__(
        self,
        knowledge_storage: KnowledgeStorage,
        api_provider_service: ApiProviderService,
        subscription_service: SubscriptionService
    ):
        self.knowledge_storage = knowledge_storage
        self.api_provider_service = api_provider_service
        self.subscription_service = subscription_service
        self._initialize_models()
        self._initialize_experts()
        self._initialize_rules()
    
    def _initialize_models(self):
        """初始化内置模型档案"""
        existing_models = self.knowledge_storage.load_model_profiles()
        if not existing_models:
            self.knowledge_storage.save_model_profiles(BUILTIN_MODEL_PROFILES)
    
    def _initialize_experts(self):
        """初始化内置业务专家"""
        existing_experts = self.knowledge_storage.load_business_experts()
        if not existing_experts:
            self.knowledge_storage.save_business_experts(BUILTIN_BUSINESS_EXPERTS)
    
    def _initialize_rules(self):
        """初始化内置路由规则"""
        existing_rules = self.knowledge_storage.load_model_route_rules()
        if not existing_rules:
            self.knowledge_storage.save_model_route_rules(BUILTIN_ROUTE_RULES)
    
    def get_model_profiles(self) -> List[Dict[str, Any]]:
        """获取所有模型档案"""
        model_dicts = self.knowledge_storage.load_model_profiles()
        return [m.to_dict() for m in model_dicts] if model_dicts else []
    
    def get_model_profile(self, model_id: str) -> Optional[Dict[str, Any]]:
        """获取指定模型档案"""
        models = self.knowledge_storage.load_model_profiles()
        for model in models:
            if model.model_id == model_id:
                return model.to_dict()
        return None
    
    def create_model_profile(
        self,
        provider_id: str,
        model_name: str,
        provider_type: str,
        model_tier: str,
        capability_tags: List[str],
        supported_task_types: List[str],
        cost_level: str,
        quality_level: str,
        speed_level: str,
        privacy_level: str,
        supports_local_only: bool,
        supports_streaming: bool,
        supports_batch: bool,
        supports_rag: bool,
        supports_image: bool,
        supports_text: bool
    ) -> Dict[str, Any]:
        """创建模型档案"""
        model = ModelProfile(
            model_id=str(uuid.uuid4()),
            provider_id=provider_id,
            model_name=model_name,
            provider_type=provider_type,
            model_tier=model_tier,
            capability_tags=capability_tags,
            supported_task_types=supported_task_types,
            cost_level=cost_level,
            quality_level=quality_level,
            speed_level=speed_level,
            privacy_level=privacy_level,
            supports_local_only=supports_local_only,
            supports_streaming=supports_streaming,
            supports_batch=supports_batch,
            supports_rag=supports_rag,
            supports_image=supports_image,
            supports_text=supports_text,
            enabled=True
        )
        
        models = self.knowledge_storage.load_model_profiles()
        models.append(model)
        self.knowledge_storage.save_model_profiles(models)
        
        return model.to_dict()
    
    def get_business_experts(self) -> List[Dict[str, Any]]:
        """获取所有业务专家"""
        expert_dicts = self.knowledge_storage.load_business_experts()
        return [e.to_dict() for e in expert_dicts] if expert_dicts else []
    
    def get_business_expert(self, expert_id: str) -> Optional[Dict[str, Any]]:
        """获取指定业务专家"""
        experts = self.knowledge_storage.load_business_experts()
        for expert in experts:
            if expert.expert_id == expert_id:
                return expert.to_dict()
        return None
    
    def create_business_expert(
        self,
        expert_name: str,
        expert_type: str,
        supported_task_types: List[str],
        capability_tags: List[str],
        risk_level: str,
        default_priority: int
    ) -> Dict[str, Any]:
        """创建业务专家"""
        expert = BusinessExpert(
            expert_id=str(uuid.uuid4()),
            expert_name=expert_name,
            expert_type=expert_type,
            supported_task_types=supported_task_types,
            capability_tags=capability_tags,
            risk_level=risk_level,
            default_priority=default_priority,
            enabled=True
        )
        
        experts = self.knowledge_storage.load_business_experts()
        experts.append(expert)
        self.knowledge_storage.save_business_experts(experts)
        
        return expert.to_dict()
    
    def get_route_rules(self) -> List[Dict[str, Any]]:
        """获取所有路由规则"""
        rule_dicts = self.knowledge_storage.load_model_route_rules()
        return [r.to_dict() for r in rule_dicts] if rule_dicts else []
    
    def get_route_rule(self, rule_id: str) -> Optional[Dict[str, Any]]:
        """获取指定路由规则"""
        rules = self.knowledge_storage.load_model_route_rules()
        for rule in rules:
            if rule.rule_id == rule_id:
                return rule.to_dict()
        return None
    
    def create_route_rule(
        self,
        task_type: str,
        feature_name: str,
        route_policy: str,
        preferred_expert_ids: List[str],
        preferred_model_ids: List[str],
        fallback_model_ids: List[str],
        min_quality_level: Optional[str] = None,
        max_cost_level: Optional[str] = None,
        local_only_required: bool = False,
        human_approval_required: bool = False
    ) -> Dict[str, Any]:
        """创建路由规则"""
        rule = ModelRouteRule(
            rule_id=str(uuid.uuid4()),
            task_type=task_type,
            feature_name=feature_name,
            route_policy=route_policy,
            preferred_expert_ids=preferred_expert_ids,
            preferred_model_ids=preferred_model_ids,
            fallback_model_ids=fallback_model_ids,
            min_quality_level=min_quality_level,
            max_cost_level=max_cost_level,
            local_only_required=local_only_required,
            human_approval_required=human_approval_required,
            enabled=True
        )
        
        rules = self.knowledge_storage.load_model_route_rules()
        rules.append(rule)
        self.knowledge_storage.save_model_route_rules(rules)
        
        return rule.to_dict()
    
    def classify_task(self, task_text: str, feature_name: Optional[str] = None) -> Dict[str, Any]:
        """识别任务类型"""
        task_type = TaskType.UNKNOWN.value
        
        # 基于特征名称识别
        if feature_name:
            if feature_name == "title_generation":
                task_type = TaskType.TITLE_GENERATION.value
            elif feature_name == "keyword_generation":
                task_type = TaskType.KEYWORD_GENERATION.value
            elif feature_name == "xiaohongshu_generation":
                task_type = TaskType.XIAOHONGSHU_GENERATION.value
            elif feature_name == "video_script_generation":
                task_type = TaskType.VIDEO_SCRIPT_GENERATION.value
            elif feature_name == "detail_page_generation":
                task_type = TaskType.DETAIL_PAGE_GENERATION.value
            elif feature_name == "image_prompt_generation":
                task_type = TaskType.IMAGE_PROMPT_GENERATION.value
            elif feature_name == "remove_bg":
                task_type = TaskType.REMOVE_BG.value
            elif feature_name == "workflow_execution":
                task_type = TaskType.WORKFLOW_EXECUTION.value
            elif feature_name == "knowledge_qa":
                task_type = TaskType.KNOWLEDGE_QA.value
            elif feature_name == "operations_analysis":
                task_type = TaskType.OPERATIONS_ANALYSIS.value
            elif feature_name == "advanced_analysis":
                task_type = TaskType.ADVANCED_ANALYSIS.value
            elif feature_name == "risk_check":
                task_type = TaskType.RISK_CHECK.value
        else:
            # 基于任务文本简单识别
            task_lower = task_text.lower()
            if "标题" in task_text or "title" in task_lower:
                task_type = TaskType.TITLE_GENERATION.value
            elif "关键词" in task_text or "keyword" in task_lower:
                task_type = TaskType.KEYWORD_GENERATION.value
            elif "详情" in task_text or "detail" in task_lower:
                task_type = TaskType.DETAIL_PAGE_GENERATION.value
            elif "运营" in task_text or "operation" in task_lower:
                task_type = TaskType.OPERATIONS_ANALYSIS.value
            elif "小红书" in task_text:
                task_type = TaskType.XIAOHONGSHU_GENERATION.value
            elif "视频脚本" in task_text or "script" in task_lower:
                task_type = TaskType.VIDEO_SCRIPT_GENERATION.value
            elif "知识" in task_text or "knowledge" in task_lower:
                task_type = TaskType.KNOWLEDGE_QA.value
            elif "图片" in task_text or "image" in task_lower:
                task_type = TaskType.IMAGE_PROMPT_GENERATION.value
        
        return {
            "task_type": task_type,
            "task_text": task_text,
            "feature_name": feature_name
        }
    
    def route(
        self,
        task_text: str,
        task_type: Optional[str] = None,
        feature_name: Optional[str] = None,
        customer_id: Optional[str] = None,
        account_id: Optional[str] = None,
        route_policy: Optional[str] = None,
        local_only: bool = False,
        high_risk: bool = False
    ) -> Dict[str, Any]:
        """路由决策"""
        # 识别任务类型
        if not task_type:
            classification = self.classify_task(task_text, feature_name)
            task_type = classification["task_type"]
        
        # 获取路由规则
        rule = self._get_rule_by_task(task_type, feature_name)
        if not rule:
            return {
                "error": "No routing rule found for this task type"
            }
        
        if not rule.enabled:
            return {
                "error": "Routing rule is disabled"
            }
        
        # 确定路由策略
        if route_policy:
            effective_policy = route_policy
        else:
            effective_policy = rule.route_policy
        
        # 如果是高风险或策略指定本地优先
        if local_only or effective_policy == RoutePolicy.LOCAL_ONLY.value:
            effective_policy = RoutePolicy.LOCAL_ONLY.value
        
        # 检查高风险功能
        if feature_name and feature_name in HIGH_RISK_FEATURES:
            return self._create_blocked_decision(
                task_text=task_text,
                task_type=task_type,
                feature_name=feature_name,
                customer_id=customer_id,
                account_id=account_id,
                route_policy=effective_policy,
                blocked_reason="High risk feature requires manual approval"
            )
        
        # 获取可用模型
        available_models = self._get_available_models(rule, effective_policy)
        
        if not available_models:
            return self._create_blocked_decision(
                task_text=task_text,
                task_type=task_type,
                feature_name=feature_name,
                customer_id=customer_id,
                account_id=account_id,
                route_policy=effective_policy,
                blocked_reason="No available models matching the routing policy"
            )
        
        # 选择模型
        selected_model = self._select_model(available_models, effective_policy, rule)
        
        # 获取激活的专家
        selected_experts = self._get_activated_experts(rule.preferred_expert_ids)
        
        # 估算点数
        estimated_points = self._estimate_points(feature_name)
        
        # 检查点数
        if account_id:
            check_result = self.subscription_service.check_points(
                customer_id=customer_id if customer_id else "unknown",
                feature_name=feature_name if feature_name else task_type,
                points_required=estimated_points
            )
            if not check_result.get("can_consume"):
                return self._create_blocked_decision(
                    task_text=task_text,
                    task_type=task_type,
                    feature_name=feature_name,
                    customer_id=customer_id,
                    account_id=account_id,
                    route_policy=effective_policy,
                    blocked_reason=check_result.get("reason", "Insufficient points")
                )
        
        # 创建决策记录
        decision = self._create_decision(
            task_text=task_text,
            task_type=task_type,
            feature_name=feature_name,
            customer_id=customer_id,
            account_id=account_id,
            route_policy=effective_policy,
            selected_expert_ids=[e.expert_id for e in selected_experts],
            candidate_model_ids=[m.model_id for m in available_models],
            selected_model_id=selected_model.model_id,
            fallback_model_ids=rule.fallback_model_ids,
            estimated_points=estimated_points,
            estimated_cost_level=selected_model.cost_level,
            requires_human_approval=rule.human_approval_required or high_risk,
            status="success",
            blocked_reason=None,
            decision_reason=f"Routed to {selected_model.model_name} based on {effective_policy} policy"
        )
        
        return decision.to_dict()
    
    def get_route_decisions(self) -> List[Dict[str, Any]]:
        """获取路由决策记录"""
        decision_dicts = self.knowledge_storage.load_model_route_decisions()
        return [d.to_dict() for d in decision_dicts] if decision_dicts else []
    
    def get_route_decision(self, decision_id: str) -> Optional[Dict[str, Any]]:
        """获取指定路由决策记录"""
        decisions = self.knowledge_storage.load_model_route_decisions()
        for decision in decisions:
            if decision.decision_id == decision_id:
                return decision.to_dict()
        return None
    
    def _get_rule_by_task(self, task_type: str, feature_name: Optional[str] = None) -> Optional[ModelRouteRule]:
        """根据任务类型获取路由规则"""
        rules = self.knowledge_storage.load_model_route_rules()
        for rule in rules:
            if rule.task_type == task_type and rule.enabled:
                if feature_name is None or rule.feature_name == feature_name:
                    return rule
        return None
    
    def _get_available_models(self, rule: ModelRouteRule, policy: str) -> List[ModelProfile]:
        """获取可用模型"""
        all_models = self.knowledge_storage.load_model_profiles()
        available = []
        
        for model in all_models:
            if not model.enabled:
                continue
            
            # 检查provider是否启用
            provider = self.api_provider_service.get_provider(model.provider_id)
            if not provider or not provider.get("enabled"):
                continue
            
            # 检查local_only策略
            if policy == RoutePolicy.LOCAL_ONLY.value and not model.supports_local_only:
                continue
            
            # 检查成本等级
            if rule.max_cost_level and self._compare_cost_level(model.cost_level, rule.max_cost_level) > 0:
                continue
            
            # 检查质量等级
            if rule.min_quality_level and self._compare_quality_level(model.quality_level, rule.min_quality_level) < 0:
                continue
            
            available.append(model)
        
        return available
    
    def _select_model(self, available_models: List[ModelProfile], policy: str, rule: ModelRouteRule) -> ModelProfile:
        """选择模型"""
        # 优先选择preferred_model_ids中的模型
        for model_id in rule.preferred_model_ids:
            for model in available_models:
                if model.model_id == model_id:
                    return model
        
        # 根据策略选择
        if policy == RoutePolicy.COST_FIRST.value:
            # 选择成本最低的
            available_models.sort(key=lambda m: self._cost_level_value(m.cost_level))
        elif policy == RoutePolicy.QUALITY_FIRST.value:
            # 选择质量最高的
            available_models.sort(key=lambda m: self._quality_level_value(m.quality_level), reverse=True)
        elif policy == RoutePolicy.SPEED_FIRST.value:
            # 选择速度最快的
            available_models.sort(key=lambda m: self._speed_level_value(m.speed_level), reverse=True)
        
        return available_models[0] if available_models else None
    
    def _get_activated_experts(self, expert_ids: List[str]) -> List[BusinessExpert]:
        """获取激活的专家"""
        all_experts = self.knowledge_storage.load_business_experts()
        activated = []
        
        for expert_id in expert_ids:
            for expert in all_experts:
                if expert.expert_id == expert_id and expert.enabled:
                    activated.append(expert)
        
        return activated
    
    def _estimate_points(self, feature_name: Optional[str]) -> int:
        """估算点数"""
        # 简单的点数估算逻辑
        point_map = {
            "title_generation": 1,
            "keyword_generation": 1,
            "xiaohongshu_generation": 3,
            "video_script_generation": 5,
            "detail_page_generation": 10,
            "workflow_execution": 5,
            "remove_bg": 10,
            "image_prompt_generation": 5,
            "knowledge_qa": 2,
            "operations_analysis": 20,
            "advanced_analysis": 20,
            "risk_check": 1
        }
        
        return point_map.get(feature_name, 1) if feature_name else 1
    
    def _compare_cost_level(self, level1: str, level2: str) -> int:
        """比较成本等级"""
        order = {CostLevel.LOW.value: 0, CostLevel.MEDIUM.value: 1, CostLevel.HIGH.value: 2}
        return order.get(level1, 0) - order.get(level2, 0)
    
    def _compare_quality_level(self, level1: str, level2: str) -> int:
        """比较质量等级"""
        order = {QualityLevel.LOW.value: 0, QualityLevel.MEDIUM.value: 1, QualityLevel.HIGH.value: 2}
        return order.get(level1, 0) - order.get(level2, 0)
    
    def _cost_level_value(self, level: str) -> int:
        """获取成本等级数值"""
        order = {CostLevel.LOW.value: 0, CostLevel.MEDIUM.value: 1, CostLevel.HIGH.value: 2}
        return order.get(level, 0)
    
    def _quality_level_value(self, level: str) -> int:
        """获取质量等级数值"""
        order = {QualityLevel.LOW.value: 0, QualityLevel.MEDIUM.value: 1, QualityLevel.HIGH.value: 2}
        return order.get(level, 0)
    
    def _speed_level_value(self, level: str) -> int:
        """获取速度等级数值"""
        order = {"fast": 2, "medium": 1, "slow": 0}
        return order.get(level, 0)
    
    def _create_decision(
        self,
        task_text: str,
        task_type: str,
        feature_name: Optional[str],
        customer_id: Optional[str],
        account_id: Optional[str],
        route_policy: str,
        selected_expert_ids: List[str],
        candidate_model_ids: List[str],
        selected_model_id: Optional[str],
        fallback_model_ids: List[str],
        estimated_points: int,
        estimated_cost_level: str,
        requires_human_approval: bool,
        status: str,
        blocked_reason: Optional[str],
        decision_reason: str
    ) -> ModelRouteDecision:
        """创建决策记录"""
        decision = ModelRouteDecision(
            decision_id=str(uuid.uuid4()),
            task_text=task_text,
            task_type=task_type,
            feature_name=feature_name,
            customer_id=customer_id,
            account_id=account_id,
            route_policy=route_policy,
            selected_expert_ids=selected_expert_ids,
            candidate_model_ids=candidate_model_ids,
            selected_model_id=selected_model_id,
            fallback_model_ids=fallback_model_ids,
            estimated_points=estimated_points,
            estimated_cost_level=estimated_cost_level,
            requires_human_approval=requires_human_approval,
            status=status,
            blocked_reason=blocked_reason,
            decision_reason=decision_reason
        )
        
        # 保存决策记录
        decisions = self.knowledge_storage.load_model_route_decisions()
        decisions.append(decision)
        self.knowledge_storage.save_model_route_decisions(decisions)
        
        return decision
    
    def _create_blocked_decision(
        self,
        task_text: str,
        task_type: str,
        feature_name: Optional[str],
        customer_id: Optional[str],
        account_id: Optional[str],
        route_policy: str,
        blocked_reason: str
    ) -> Dict[str, Any]:
        """创建阻断决策"""
        decision = self._create_decision(
            task_text=task_text,
            task_type=task_type,
            feature_name=feature_name,
            customer_id=customer_id,
            account_id=account_id,
            route_policy=route_policy,
            selected_expert_ids=[],
            candidate_model_ids=[],
            selected_model_id=None,
            fallback_model_ids=[],
            estimated_points=0,
            estimated_cost_level=CostLevel.LOW.value,
            requires_human_approval=False,
            status="blocked",
            blocked_reason=blocked_reason,
            decision_reason=blocked_reason
        )
        
        return decision.to_dict()
