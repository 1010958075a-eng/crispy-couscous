"""
产品B v1.2 - 套餐额度中心/AI点数系统服务
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.subscription import (
    SubscriptionPlan,
    CustomerQuotaAccount,
    FeaturePointRule,
    UsageRecord,
    BUILTIN_PLANS,
    BUILTIN_FEATURE_RULES,
    HIGH_RISK_FEATURES,
    AccountStatus,
    UsageStatus
)
from .knowledge_storage import KnowledgeStorage


class SubscriptionService:
    """订阅额度中心服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
        self._initialize_plans()
        self._initialize_rules()
    
    def _initialize_plans(self):
        """初始化内置套餐"""
        existing_plans = self.knowledge_storage.load_subscription_plans()
        if not existing_plans:
            # 如果不存在，创建并保存内置套餐
            self.knowledge_storage.save_subscription_plans(BUILTIN_PLANS)
    
    def _initialize_rules(self):
        """初始化内置扣点规则"""
        existing_rules = self.knowledge_storage.load_feature_point_rules()
        if not existing_rules:
            # 如果不存在，创建并保存内置规则
            self.knowledge_storage.save_feature_point_rules(BUILTIN_FEATURE_RULES)
    
    def get_plans(self) -> List[Dict[str, Any]]:
        """获取所有套餐"""
        plan_dicts = self.knowledge_storage.load_subscription_plans()
        return [p.to_dict() for p in plan_dicts] if plan_dicts else []
    
    def get_plan(self, plan_id: str) -> Optional[Dict[str, Any]]:
        """获取指定套餐"""
        plans = self.knowledge_storage.load_subscription_plans()
        for plan in plans:
            if plan.plan_id == plan_id:
                return plan.to_dict()
        return None
    
    def create_plan(
        self,
        plan_name: str,
        plan_level: str,
        monthly_price: float,
        included_points: int,
        daily_point_limit: int,
        monthly_point_limit: int,
        image_generation_limit: int,
        remove_bg_limit: int,
        workflow_limit: int,
        knowledge_base_limit: int,
        advanced_model_enabled: bool,
        team_member_limit: int,
        private_deployment_enabled: bool
    ) -> Dict[str, Any]:
        """创建套餐"""
        plan = SubscriptionPlan(
            plan_id=str(uuid.uuid4()),
            plan_name=plan_name,
            plan_level=plan_level,
            monthly_price=monthly_price,
            included_points=included_points,
            daily_point_limit=daily_point_limit,
            monthly_point_limit=monthly_point_limit,
            image_generation_limit=image_generation_limit,
            remove_bg_limit=remove_bg_limit,
            workflow_limit=workflow_limit,
            knowledge_base_limit=knowledge_base_limit,
            advanced_model_enabled=advanced_model_enabled,
            team_member_limit=team_member_limit,
            private_deployment_enabled=private_deployment_enabled,
            enabled=True
        )
        
        plans = self.knowledge_storage.load_subscription_plans()
        plans.append(plan)
        self.knowledge_storage.save_subscription_plans(plans)
        
        return plan.to_dict()
    
    def create_customer_account(
        self,
        customer_id: str,
        plan_id: str
    ) -> Dict[str, Any]:
        """创建客户额度账户"""
        # 获取套餐信息
        plan = self._get_plan_object(plan_id)
        if not plan:
            raise ValueError("Plan not found")
        
        if not plan.enabled:
            raise ValueError("Plan is disabled")
        
        account = CustomerQuotaAccount(
            account_id=str(uuid.uuid4()),
            customer_id=customer_id,
            plan_id=plan_id,
            total_points=plan.included_points,
            used_points=0,
            remaining_points=plan.included_points,
            daily_used_points=0,
            monthly_used_points=0,
            status=AccountStatus.ACTIVE.value
        )
        
        accounts = self.knowledge_storage.load_customer_quota_accounts()
        accounts.append(account)
        self.knowledge_storage.save_customer_quota_accounts(accounts)
        
        return account.to_dict()
    
    def get_account(self, account_id: str) -> Optional[Dict[str, Any]]:
        """获取指定账户"""
        accounts = self.knowledge_storage.load_customer_quota_accounts()
        for account in accounts:
            if account.account_id == account_id:
                return account.to_dict()
        return None
    
    def get_account_by_customer(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """按客户ID获取账户"""
        accounts = self.knowledge_storage.load_customer_quota_accounts()
        for account in accounts:
            if account.customer_id == customer_id:
                return account.to_dict()
        return None
    
    def get_feature_rules(self) -> List[Dict[str, Any]]:
        """获取所有扣点规则"""
        rule_dicts = self.knowledge_storage.load_feature_point_rules()
        return [r.to_dict() for r in rule_dicts] if rule_dicts else []
    
    def get_feature_rule(self, feature_name: str) -> Optional[Dict[str, Any]]:
        """获取指定功能的扣点规则"""
        rules = self.knowledge_storage.load_feature_point_rules()
        for rule in rules:
            if rule.feature_name == feature_name:
                return rule.to_dict()
        return None
    
    def create_feature_rule(
        self,
        feature_name: str,
        points_required: int,
        feature_type: str,
        risk_level: str
    ) -> Dict[str, Any]:
        """创建扣点规则"""
        rule = FeaturePointRule(
            rule_id=str(uuid.uuid4()),
            feature_name=feature_name,
            points_required=points_required,
            feature_type=feature_type,
            risk_level=risk_level,
            enabled=True
        )
        
        rules = self.knowledge_storage.load_feature_point_rules()
        rules.append(rule)
        self.knowledge_storage.save_feature_point_rules(rules)
        
        return rule.to_dict()
    
    def check_points(
        self,
        customer_id: str,
        feature_name: str,
        points_required: int
    ) -> Dict[str, Any]:
        """检查点数是否足够"""
        # 获取账户
        account = self._get_account_by_customer(customer_id)
        if not account:
            return {
                "can_consume": False,
                "reason": "Account not found"
            }
        
        if account.status != AccountStatus.ACTIVE.value:
            return {
                "can_consume": False,
                "reason": f"Account status is {account.status}"
            }
        
        # 获取套餐
        plan = self._get_plan_object(account.plan_id)
        if not plan:
            return {
                "can_consume": False,
                "reason": "Plan not found"
            }
        
        if not plan.enabled:
            return {
                "can_consume": False,
                "reason": "Plan is disabled"
            }
        
        # 检查点数是否足够
        if account.remaining_points < points_required:
            return {
                "can_consume": False,
                "reason": "Insufficient points",
                "remaining_points": account.remaining_points,
                "points_required": points_required
            }
        
        # 检查日限制
        if account.daily_used_points + points_required > plan.daily_point_limit:
            return {
                "can_consume": False,
                "reason": "Daily point limit exceeded",
                "daily_used_points": account.daily_used_points,
                "daily_limit": plan.daily_point_limit,
                "points_required": points_required
            }
        
        # 检查月限制
        if account.monthly_used_points + points_required > plan.monthly_point_limit:
            return {
                "can_consume": False,
                "reason": "Monthly point limit exceeded",
                "monthly_used_points": account.monthly_used_points,
                "monthly_limit": plan.monthly_point_limit,
                "points_required": points_required
            }
        
        # 检查功能规则是否启用
        rule = self._get_rule_by_feature(feature_name)
        if not rule:
            return {
                "can_consume": False,
                "reason": "Feature rule not found"
            }
        
        if not rule.enabled:
            return {
                "can_consume": False,
                "reason": "Feature rule is disabled"
            }
        
        # 检查高风险功能
        if feature_name in HIGH_RISK_FEATURES:
            return {
                "can_consume": False,
                "reason": "High risk feature requires manual confirmation"
            }
        
        return {
            "can_consume": True,
            "remaining_points": account.remaining_points,
            "points_required": points_required
        }
    
    def mock_consume(
        self,
        customer_id: str,
        feature_name: str
    ) -> Dict[str, Any]:
        """模拟扣点（不真实扣款）"""
        # 获取账户
        account = self._get_account_by_customer(customer_id)
        if not account:
            return {
                "error": "Account not found"
            }
        
        # 获取规则
        rule = self._get_rule_by_feature(feature_name)
        if not rule:
            return {
                "error": "Feature rule not found"
            }
        
        points_required = rule.points_required
        
        # 检查点数
        check_result = self.check_points(customer_id, feature_name, points_required)
        if not check_result.get("can_consume"):
            # 创建失败的消费记录
            usage_record = self._create_usage_record(
                customer_id=customer_id,
                account_id=account.account_id,
                plan_id=account.plan_id,
                feature_name=feature_name,
                points_used=points_required,
                status=UsageStatus.BLOCKED.value,
                blocked_reason=check_result.get("reason"),
                before_remaining_points=account.remaining_points,
                after_remaining_points=account.remaining_points
            )
            return usage_record.to_dict()
        
        # 执行扣点
        before_remaining = account.remaining_points
        account.remaining_points -= points_required
        account.used_points += points_required
        account.daily_used_points += points_required
        account.monthly_used_points += points_required
        account.updated_at = datetime.now()
        
        # 更新账户
        self._update_account(account)
        
        # 创建成功的消费记录
        usage_record = self._create_usage_record(
            customer_id=customer_id,
            account_id=account.account_id,
            plan_id=account.plan_id,
            feature_name=feature_name,
            points_used=points_required,
            status=UsageStatus.SUCCESS.value,
            before_remaining_points=before_remaining,
            after_remaining_points=account.remaining_points
        )
        
        return usage_record.to_dict()
    
    def get_usage_records(self) -> List[Dict[str, Any]]:
        """获取消费记录"""
        usage_dicts = self.knowledge_storage.load_usage_records()
        return [u.to_dict() for u in usage_dicts] if usage_dicts else []
    
    def get_usage_record(self, usage_id: str) -> Optional[Dict[str, Any]]:
        """获取指定消费记录"""
        usage_records = self.knowledge_storage.load_usage_records()
        for record in usage_records:
            if record.usage_id == usage_id:
                return record.to_dict()
        return None
    
    def _get_plan_object(self, plan_id: str) -> Optional[SubscriptionPlan]:
        """获取套餐对象"""
        plans = self.knowledge_storage.load_subscription_plans()
        for plan in plans:
            if plan.plan_id == plan_id:
                return plan
        return None
    
    def _get_account_by_customer(self, customer_id: str) -> Optional[CustomerQuotaAccount]:
        """按客户ID获取账户对象"""
        accounts = self.knowledge_storage.load_customer_quota_accounts()
        for account in accounts:
            if account.customer_id == customer_id:
                return account
        return None
    
    def _get_account_object(self, account_id: str) -> Optional[CustomerQuotaAccount]:
        """获取账户对象"""
        accounts = self.knowledge_storage.load_customer_quota_accounts()
        for account in accounts:
            if account.account_id == account_id:
                return account
        return None
    
    def _get_rule_by_feature(self, feature_name: str) -> Optional[FeaturePointRule]:
        """按功能名称获取规则对象"""
        rules = self.knowledge_storage.load_feature_point_rules()
        for rule in rules:
            if rule.feature_name == feature_name:
                return rule
        return None
    
    def _update_account(self, account: CustomerQuotaAccount):
        """更新账户"""
        accounts = self.knowledge_storage.load_customer_quota_accounts()
        for i, acc in enumerate(accounts):
            if acc.account_id == account.account_id:
                accounts[i] = account
                break
        self.knowledge_storage.save_customer_quota_accounts(accounts)
    
    def _create_usage_record(
        self,
        customer_id: str,
        account_id: str,
        plan_id: str,
        feature_name: str,
        points_used: int,
        status: str,
        blocked_reason: Optional[str] = None,
        before_remaining_points: int = 0,
        after_remaining_points: int = 0
    ) -> UsageRecord:
        """创建消费记录"""
        usage_record = UsageRecord(
            usage_id=str(uuid.uuid4()),
            customer_id=customer_id,
            account_id=account_id,
            plan_id=plan_id,
            feature_name=feature_name,
            points_used=points_used,
            status=status,
            blocked_reason=blocked_reason,
            before_remaining_points=before_remaining_points,
            after_remaining_points=after_remaining_points
        )
        
        # 保存消费记录
        usage_records = self.knowledge_storage.load_usage_records()
        usage_records.append(usage_record)
        self.knowledge_storage.save_usage_records(usage_records)
        
        return usage_record
