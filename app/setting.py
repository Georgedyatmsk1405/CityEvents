import os
from typing import Dict, Any, Literal, Annotated

import yaml
from pydantic import BaseModel, Field, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict


class MyBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )


class OpenAISettings(MyBaseSettings):
    openai_api_key: str = Field(..., description="OpenAI API key", validation_alias="OPENAI_API_KEY")
    openai_base_url: str = Field(..., description="OpenAI base URL", validation_alias="OPENAI_BASE_URL")


class SearchSettings(MyBaseSettings):
    search_api_key: str = Field(..., description="Yandex Search API key", validation_alias="SEARCH_API_KEY")
    search_mcp_url: str = Field(..., description="Yandex Search MCP url", validation_alias="YANDEX_SEARCH_MCP_URL")





class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )
    
    # Sub-settings
    openai: OpenAISettings = OpenAISettings()
    search: SearchSettings = SearchSettings()
    
    # YAML config paths
    config_path: str = os.path.join(os.path.dirname(__file__), "config.yaml")
    prompts_path: str = os.path.join(os.path.dirname(__file__), "prompts.yaml")

    def load_config(self) -> Dict[str, Dict[str, str]]:
        with open(self.config_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f) or {}
        return data

    def load_prompts(self) -> Dict[str, Dict[str, str]]:
        with open(self.prompts_path, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = yaml.safe_load(f) or {}
        return data


def build_settings() -> Settings:
    """Создаёт Settings с валидацией."""
    try:
        return Settings()
    except ValidationError as exc:
        print(f"❌ Configuration error:\n{exc}")
        raise


# Load once for app-wide import
_settings = build_settings()
_config = _settings.load_config()
_prompts = _settings.load_prompts()

# Expose for backward compatibility
llm_settings: OpenAISettings = _settings.openai
agents_settings: Dict[str, Dict[str, str]] = _config
agents_prompts: Dict[str, Dict[str, str]] = _prompts


