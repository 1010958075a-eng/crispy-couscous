"""
产品B v1.1 - API供应商中心服务
"""

import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime

from models.api_provider import (
    ApiProvider,
    ApiCallRecord,
    ApiQuotaRecord,
    BUILTIN_PROVIDERS,
    HIGH_RISK_KEYWORDS,
    HIGH_RISK_PROVIDER_TYPES,
    CallStatus,
    RiskLevel
)
from .knowledge_storage import KnowledgeStorage


class ApiProviderService:
    """API供应商中心服务"""
    
    def __init__(self, knowledge_storage: KnowledgeStorage):
        self.knowledge_storage = knowledge_storage
        self._initialize_providers()
    
    def _initialize_providers(self):
        """初始化内置供应商"""
        existing_providers = self.knowledge_storage.load_api_providers()
        if not existing_providers:
            # 如果不存在，创建并保存内置供应商
            self.knowledge_storage.save_api_providers(BUILTIN_PROVIDERS)
    
    def get_providers(self) -> List[Dict[str, Any]]:
        """获取所有供应商"""
        provider_dicts = self.knowledge_storage.load_api_providers()
        return [p.to_dict() for p in provider_dicts] if provider_dicts else []
    
    def get_provider(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """获取指定供应商"""
        providers = self.knowledge_storage.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                return provider.to_dict()
        return None
    
    def create_provider(
        self,
        provider_name: str,
        provider_type: str,
        model_name: Optional[str],
        api_base_url: Optional[str],
        api_key_placeholder: Optional[str],
        cost_level: str,
        risk_level: str,
        daily_limit: int,
        monthly_limit: int,
        unit_cost_estimate: float,
        supported_features: List[str],
        fallback_provider_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """创建供应商配置"""
        # 检查是否保存真实API Key
        if api_key_placeholder and not self._is_placeholder_key(api_key_placeholder):
            raise ValueError("不允许保存真实API Key，只保存placeholder或masked key")
        
        provider = ApiProvider(
            provider_id=str(uuid.uuid4()),
            provider_name=provider_name,
            provider_type=provider_type,
            model_name=model_name,
            api_base_url=api_base_url,
            api_key_placeholder=api_key_placeholder,
            cost_level=cost_level,
            risk_level=risk_level,
            enabled=True,
            daily_limit=daily_limit,
            monthly_limit=monthly_limit,
            unit_cost_estimate=unit_cost_estimate,
            supported_features=supported_features,
            fallback_provider_id=fallback_provider_id
        )
        
        providers = self.knowledge_storage.load_api_providers()
        providers.append(provider)
        self.knowledge_storage.save_api_providers(providers)
        
        return provider.to_dict()
    
    def _is_placeholder_key(self, api_key: str) -> bool:
        """检查是否为placeholder key"""
        placeholder_patterns = [
            "sk-xxxxxxxx",
            "xxxxxxxxxxxx",
            "sk-placeholder",
            "placeholder",
            "masked",
            "ak-xxxxxxxx"
        ]
        return any(pattern in api_key.lower() for pattern in placeholder_patterns)
    
    def enable_provider(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """启用供应商"""
        providers = self.knowledge_storage.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                provider.enabled = True
                provider.updated_at = datetime.now()
                self.knowledge_storage.save_api_providers(providers)
                return provider.to_dict()
        return None
    
    def disable_provider(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """禁用供应商"""
        providers = self.knowledge_storage.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                provider.enabled = False
                provider.updated_at = datetime.now()
                self.knowledge_storage.save_api_providers(providers)
                return provider.to_dict()
        return None
    
    def set_quota(
        self,
        provider_id: str,
        daily_limit: int,
        monthly_limit: int
    ) -> Optional[Dict[str, Any]]:
        """设置额度"""
        providers = self.knowledge_storage.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                provider.daily_limit = daily_limit
                provider.monthly_limit = monthly_limit
                provider.updated_at = datetime.now()
                self.knowledge_storage.save_api_providers(providers)
                
                # 更新额度记录
                self._update_quota_record(provider)
                
                return provider.to_dict()
        return None
    
    def _update_quota_record(self, provider: ApiProvider):
        """更新额度记录"""
        quota_records = self.knowledge_storage.load_api_quota_records()
        
        # 查找现有记录
        quota_record = None
        for record in quota_records:
            if record.provider_id == provider.provider_id:
                quota_record = record
                break
        
        if quota_record:
            # 更新现有记录
            quota_record.daily_limit = provider.daily_limit
            quota_record.monthly_limit = provider.monthly_limit
            quota_record.used_today = provider.used_today
            quota_record.used_this_month = provider.used_this_month
            quota_record.remaining_today = provider.daily_limit - provider.used_today
            quota_record.remaining_this_month = provider.monthly_limit - provider.used_this_month
            quota_record.updated_at = datetime.now()
        else:
            # 创建新记录
            quota_record = ApiQuotaRecord(
                quota_id=str(uuid.uuid4()),
                provider_id=provider.provider_id,
                daily_limit=provider.daily_limit,
                monthly_limit=provider.monthly_limit,
                used_today=provider.used_today,
                used_this_month=provider.used_this_month,
                remaining_today=provider.daily_limit - provider.used_today,
                remaining_this_month=provider.monthly_limit - provider.used_this_month
            )
            quota_records.append(quota_record)
        
        self.knowledge_storage.save_api_quota_records(quota_records)
    
    def estimate_cost(
        self,
        provider_id: str,
        feature_name: str,
        estimated_units: int
    ) -> Dict[str, Any]:
        """估算调用成本"""
        provider = self._get_provider_object(provider_id)
        if not provider:
            return {"error": "Provider not found"}
        
        estimated_cost = provider.unit_cost_estimate * estimated_units
        
        return {
            "provider_id": provider_id,
            "provider_name": provider.provider_name,
            "feature_name": feature_name,
            "estimated_units": estimated_units,
            "estimated_cost": estimated_cost,
            "currency": "USD"
        }
    
    def check_quota(
        self,
        provider_id: str,
        estimated_units: int
    ) -> Dict[str, Any]:
        """检查额度"""
        provider = self._get_provider_object(provider_id)
        if not provider:
            return {"error": "Provider not found", "can_call": False}
        
        if not provider.enabled:
            return {
                "can_call": False,
                "reason": "Provider is disabled"
            }
        
        remaining_today = provider.daily_limit - provider.used_today
        remaining_this_month = provider.monthly_limit - provider.used_this_month
        
        if remaining_today < estimated_units:
            return {
                "can_call": False,
                "reason": "Daily quota exceeded",
                "remaining_today": remaining_today,
                "estimated_units": estimated_units
            }
        
        if remaining_this_month < estimated_units:
            return {
                "can_call": False,
                "reason": "Monthly quota exceeded",
                "remaining_this_month": remaining_this_month,
                "estimated_units": estimated_units
            }
        
        return {
            "can_call": True,
            "remaining_today": remaining_today,
            "remaining_this_month": remaining_this_month
        }
    
    def mock_call(
        self,
        provider_id: str,
        feature_name: str,
        request_summary: str,
        estimated_units: int
    ) -> Dict[str, Any]:
        """模拟API调用（不真实调用外部API）"""
        provider = self._get_provider_object(provider_id)
        if not provider:
            return {"error": "Provider not found"}
        
        # 检查是否启用
        if not provider.enabled:
            call_record = self._create_call_record(
                provider_id=provider_id,
                provider_name=provider.provider_name,
                provider_type=provider.provider_type,
                feature_name=feature_name,
                request_summary=request_summary,
                estimated_units=estimated_units,
                estimated_cost=provider.unit_cost_estimate * estimated_units,
                status=CallStatus.BLOCKED.value,
                blocked_reason="Provider is disabled"
            )
            return call_record.to_dict()
        
        # 检查额度
        quota_check = self.check_quota(provider_id, estimated_units)
        if not quota_check.get("can_call"):
            call_record = self._create_call_record(
                provider_id=provider_id,
                provider_name=provider.provider_name,
                provider_type=provider.provider_type,
                feature_name=feature_name,
                request_summary=request_summary,
                estimated_units=estimated_units,
                estimated_cost=provider.unit_cost_estimate * estimated_units,
                status=CallStatus.BLOCKED.value,
                blocked_reason=quota_check.get("reason", "Quota exceeded")
            )
            return call_record.to_dict()
        
        # 检查高风险关键词
        blocked_reason = self._check_high_risk_keywords(request_summary)
        if blocked_reason:
            call_record = self._create_call_record(
                provider_id=provider_id,
                provider_name=provider.provider_name,
                provider_type=provider.provider_type,
                feature_name=feature_name,
                request_summary=request_summary,
                estimated_units=estimated_units,
                estimated_cost=provider.unit_cost_estimate * estimated_units,
                status=CallStatus.BLOCKED.value,
                blocked_reason=blocked_reason
            )
            return call_record.to_dict()
        
        # 检查高风险供应商类型
        if provider.provider_type in HIGH_RISK_PROVIDER_TYPES:
            call_record = self._create_call_record(
                provider_id=provider_id,
                provider_name=provider.provider_name,
                provider_type=provider.provider_type,
                feature_name=feature_name,
                request_summary=request_summary,
                estimated_units=estimated_units,
                estimated_cost=provider.unit_cost_estimate * estimated_units,
                status=CallStatus.BLOCKED.value,
                blocked_reason="High risk provider type"
            )
            return call_record.to_dict()
        
        # 模拟成功调用
        call_record = self._create_call_record(
            provider_id=provider_id,
            provider_name=provider.provider_name,
            provider_type=provider.provider_type,
            feature_name=feature_name,
            request_summary=request_summary,
            estimated_units=estimated_units,
            estimated_cost=provider.unit_cost_estimate * estimated_units,
            status=CallStatus.SUCCESS.value
        )
        
        # 更新使用量
        self._update_usage(provider_id, estimated_units)
        
        return call_record.to_dict()
    
    def _check_high_risk_keywords(self, text: str) -> Optional[str]:
        """检查高风险关键词"""
        for keyword in HIGH_RISK_KEYWORDS:
            if keyword in text:
                return f"High risk keyword detected: {keyword}"
        return None
    
    def _create_call_record(
        self,
        provider_id: str,
        provider_name: str,
        provider_type: str,
        feature_name: str,
        request_summary: str,
        estimated_units: int,
        estimated_cost: float,
        status: str,
        blocked_reason: Optional[str] = None
    ) -> ApiCallRecord:
        """创建调用记录"""
        call_record = ApiCallRecord(
            call_id=str(uuid.uuid4()),
            provider_id=provider_id,
            provider_name=provider_name,
            provider_type=provider_type,
            feature_name=feature_name,
            request_summary=request_summary,
            estimated_units=estimated_units,
            estimated_cost=estimated_cost,
            status=status,
            blocked_reason=blocked_reason
        )
        
        # 保存调用记录
        call_records = self.knowledge_storage.load_api_call_records()
        call_records.append(call_record)
        self.knowledge_storage.save_api_call_records(call_records)
        
        return call_record
    
    def _update_usage(self, provider_id: str, units: int):
        """更新使用量"""
        providers = self.knowledge_storage.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                provider.used_today += units
                provider.used_this_month += units
                provider.updated_at = datetime.now()
                self.knowledge_storage.save_api_providers(providers)
                
                # 更新额度记录
                self._update_quota_record(provider)
                break
    
    def _get_provider_object(self, provider_id: str) -> Optional[ApiProvider]:
        """获取供应商对象"""
        providers = self.knowledge_storage.load_api_providers()
        for provider in providers:
            if provider.provider_id == provider_id:
                return provider
        return None
    
    def get_call_records(self) -> List[Dict[str, Any]]:
        """获取调用记录"""
        call_records = self.knowledge_storage.load_api_call_records()
        return [record.to_dict() for record in call_records] if call_records else []
    
    def get_call_record(self, call_id: str) -> Optional[Dict[str, Any]]:
        """获取指定调用记录"""
        call_records = self.knowledge_storage.load_api_call_records()
        for record in call_records:
            if record.call_id == call_id:
                return record.to_dict()
        return None
    
    def get_quota_records(self) -> List[Dict[str, Any]]:
        """获取额度记录"""
        quota_records = self.knowledge_storage.load_api_quota_records()
        return [record.to_dict() for record in quota_records] if quota_records else []
