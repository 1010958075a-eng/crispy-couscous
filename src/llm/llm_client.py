"""
产品B - LLM客户端
"""

import asyncio
from typing import Optional
from abc import ABC, abstractmethod

from config.llm_config import LLMConfig, LLMProvider


class LLMClient(ABC):
    """LLM客户端抽象基类"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    @abstractmethod
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        完成文本
        
        Args:
            prompt: 提示词
            max_tokens: 最大token数
            temperature: 温度
            
        Returns:
            生成的文本
        """
        pass


class MockLLMClient(LLMClient):
    """模拟LLM客户端（用于测试）"""
    
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """模拟文本完成"""
        return """
```CODE
def example_function():
    return "Hello, World!"
```
EXPLANATION:
这是一个示例函数。
DEPENDENCIES:
- None
TESTS:
def test_example():
    assert example_function() == "Hello, World!"
"""


class OpenAILLMClient(LLMClient):
    """OpenAI LLM客户端"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            import openai
            self.openai = openai
            self.client = openai.AsyncOpenAI(
                api_key=config.api_key,
                base_url=config.openai_base_url
            )
        except ImportError as e:
            raise ImportError("请安装openai库: pip install openai") from e
    
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """使用OpenAI API完成文本"""
        try:
            response = await self.client.chat.completions.create(
                model=self.config.model or "gpt-4",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens or self.config.max_tokens,
                temperature=temperature or self.config.temperature,
                timeout=self.config.timeout
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"OpenAI API调用失败: {e}") from e


class AnthropicLLMClient(LLMClient):
    """Anthropic LLM客户端"""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            import anthropic
            self.anthropic = anthropic
            self.client = anthropic.AsyncAnthropic(
                api_key=config.api_key,
                timeout=self.config.timeout
            )
        except ImportError as e:
            raise ImportError("请安装anthropic库: pip install anthropic") from e
    
    async def complete(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """使用Anthropic API完成文本"""
        try:
            response = await self.client.messages.create(
                model=self.config.model or "claude-3-opus-20240229",
                max_tokens=max_tokens or self.config.max_tokens,
                temperature=temperature or self.config.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                anthropic_version=self.config.anthropic_version
            )
            return response.content[0].text
        except Exception as e:
            raise RuntimeError(f"Anthropic API调用失败: {e}") from e


def create_llm_client(config: Optional[LLMConfig] = None) -> LLMClient:
    """
    创建LLM客户端
    
    Args:
        config: LLM配置，如果为None则从环境变量加载
        
    Returns:
        LLM客户端实例
    """
    if config is None:
        config = LLMConfig.from_env()
    
    if config.provider == LLMProvider.OPENAI:
        return OpenAILLMClient(config)
    elif config.provider == LLMProvider.ANTHROPIC:
        return AnthropicLLMClient(config)
    else:
        return MockLLMClient(config)
