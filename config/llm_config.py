"""
产品B - LLM配置
"""

from typing import Optional
from enum import Enum
from pydantic import BaseModel, Field


class LLMProvider(str, Enum):
    """LLM提供商"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"


class LLMConfig(BaseModel):
    """LLM配置"""
    provider: LLMProvider = Field(default=LLMProvider.MOCK, description="LLM提供商")
    api_key: Optional[str] = Field(default=None, description="LLM API密钥")
    model: Optional[str] = Field(default=None, description="LLM模型名称")
    max_tokens: int = Field(default=2048, description="最大令牌数")
    temperature: float = Field(default=0.7, description="温度参数")
    timeout: int = Field(default=30, description="超时时间")

    # OpenAI特定配置
    openai_base_url: Optional[str] = Field(default=None, description="OpenAI基础URL")

    # Anthropic特定配置
    anthropic_version: str = Field(default="2023-06-01", description="Anthropic版本")

    class Config:
        extra = "ignore"  # 忽略额外的字段，避免验证错误
    
    @classmethod
    def from_env(cls) -> "LLMConfig":
        """从环境变量加载配置"""
        import os
        
        provider_str = os.getenv("LLM_PROVIDER", "mock").lower()
        provider = LLMProvider(provider_str)
        
        config = cls(
            provider=provider,
            api_key=os.getenv("LLM_API_KEY"),
            model=os.getenv("LLM_MODEL"),
            max_tokens=int(os.getenv("LLM_MAX_TOKENS", "2048")),
            temperature=float(os.getenv("LLM_TEMPERATURE", "0.7")),
            timeout=int(os.getenv("LLM_TIMEOUT", "30")),
            openai_base_url=os.getenv("OPENAI_BASE_URL"),
            anthropic_version=os.getenv("ANTHROPIC_VERSION", "2023-06-01")
        )
        
        # 设置默认模型
        if config.provider == LLMProvider.OPENAI and not config.model:
            config.model = "gpt-4"
        elif config.provider == LLMProvider.ANTHROPIC and not config.model:
            config.model = "claude-3-opus-20240229"
        
        return config
