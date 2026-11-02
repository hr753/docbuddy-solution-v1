"""All configuration comes from environment variables (or a local .env file).

There is deliberately NO default for API_KEYS: if it is missing, the app refuses to start.
That is safer than shipping a "default key" that someone forgets to change.
"""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "DocBuddy"
    version: str = "0.1.0"

    api_keys: str = Field(min_length=1, description="Comma-separated accepted API keys")
    cors_origins: str = "http://localhost:8501"
    llm_provider: str = "fake"
    stream_delay_seconds: float = Field(default=0.05, ge=0, le=1)

    @property
    def api_key_list(self) -> list[str]:
        return [k.strip() for k in self.api_keys.split(",") if k.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
