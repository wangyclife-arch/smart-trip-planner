"""LLM服务模块"""

import os

from hello_agents import HelloAgentsLLM

from ..config import get_settings

# 全局LLM实例
_llm_instance = None


def get_llm() -> HelloAgentsLLM:
    """
    获取LLM实例(单例模式)

    Returns:
        HelloAgentsLLM实例
    """
    global _llm_instance

    if _llm_instance is None:
        # 确保 .env 已加载
        get_settings()

        # 显式传入 provider/密钥/地址：
        # 避免系统级的 OPENAI_API_KEY 等变量覆盖 .env 中的 LLM_* 配置。
        _llm_instance = HelloAgentsLLM(
            provider="custom",
            model=os.getenv("LLM_MODEL_ID"),
            api_key=os.getenv("LLM_API_KEY"),
            base_url=os.getenv("LLM_BASE_URL"),
        )

        print("✅ LLM服务初始化成功")
        print(f"   提供商: {_llm_instance.provider}")
        print(f"   模型: {_llm_instance.model}")

    return _llm_instance


def reset_llm():
    """重置LLM实例(用于测试或重新配置)"""
    global _llm_instance
    _llm_instance = None