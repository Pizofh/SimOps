from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="SIMOPS_", case_sensitive=False)

    app_name: str = "SimOps API"
    service_name: str = "simops-backend"
    environment: str = "local"
    log_level: str = "INFO"
    database_url: str = Field(
        default="postgresql+psycopg://simops@localhost:5432/simops",
        description="Database connection string for SQLAlchemy.",
    )
    default_query_limit: int = 50
    max_query_limit: int = 200

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()


@lru_cache
def get_settings() -> Settings:
    return Settings()
