"""Factory helpers to build shared OpenAI provider and chat model.

Sources:
- llm_settings (from .env): OPENAI_API_KEY, OPENAI_BASE_URL
- agents_settings (from config.yaml): agents.model_name, temperature, max_tokens, top_p

Import and reuse these helpers across agents to ensure consistent model setup.
"""

from typing import Dict, Any

from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.models.openai import OpenAIChatModel, OpenAIChatModelSettings

from app.setting import llm_settings, agents_settings


def get_openai_provider() -> OpenAIProvider:
    """Create an OpenAIProvider using llm_settings (env-derived)."""
    return OpenAIProvider(
        api_key=llm_settings.openai_api_key,
        base_url=llm_settings.openai_base_url,
    )


def _get_agent_cfg() -> Dict[str, Any]:
    """Return the agent config dict from agents_settings['agents']."""
    if isinstance(agents_settings, dict):
        return agents_settings.get("agents", {}) or {}
    return {}


def get_openai_chat_model(
    model_name: str | None = None,
    *,
    temperature: float | None = None,
    max_tokens: int | None = None,
    top_p: float | None = None,
) -> OpenAIChatModel:
    """Create an OpenAIChatModel with settings resolved from YAML or overrides.

    Args:
        model_name: Optional override; falls back to agents.model_name.
        temperature: Optional override; falls back to agents.temperature.
        max_tokens: Optional override; falls back to agents.max_tokens.
        top_p: Optional override; falls back to agents.top_p.
    """
    cfg = _get_agent_cfg()
    resolved_model_name = model_name or cfg.get("model_name", "gpt-4o-mini")
    resolved_temperature = temperature if temperature is not None else cfg.get("temperature", 0.7)
    resolved_max_tokens = max_tokens if max_tokens is not None else cfg.get("max_tokens", 10000)
    resolved_top_p = top_p if top_p is not None else cfg.get("top_p", 0.95)

    provider = get_openai_provider()
    return OpenAIChatModel(
        model_name=resolved_model_name,
        provider=provider,
        settings=OpenAIChatModelSettings(
            temperature=resolved_temperature,
            max_tokens=resolved_max_tokens,
            top_p=resolved_top_p,
        ),
    )


