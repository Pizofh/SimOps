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
        default="postgresql+psycopg://simops:simops@localhost:5434/simops",
        description="Database connection string for SQLAlchemy.",
    )
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8080,http://127.0.0.1:8080"
    allowed_hosts: str = "localhost,127.0.0.1,backend,testserver"
    default_query_limit: int = 50
    max_query_limit: int = 200

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @field_validator("default_query_limit", "max_query_limit")
    @classmethod
    def validate_query_limits(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Query limits must be greater than zero")
        return value

    @property
    def allowed_host_list(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
