from __future__ import annotations

from functools import lru_cache

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    api_url: str = "http://localhost:8000/events"
    event_interval_seconds: float = Field(default=5.0, gt=0)
    failure_rate: float = Field(default=0.25, ge=0, le=1)
    burst_rate: float = Field(default=0.15, ge=0, le=1)
    burst_min_size: int = Field(default=3, ge=1)
    burst_max_size: int = Field(default=6, ge=1)
    service_names: str = "payments-api,auth-api,inventory-worker"
    environment: str = "lab"
    source: str = "simulator"
    request_timeout_seconds: float = Field(default=5.0, gt=0)
    max_random_delay_ms: int = Field(default=250, ge=0)
    service_name: str = "simops-simulator"
    log_level: str = "INFO"

    @field_validator("service_names")
    @classmethod
    def validate_service_names(cls, value: str) -> str:
        names = [item.strip() for item in value.split(",") if item.strip()]
        if not names:
            raise ValueError("SERVICE_NAMES must contain at least one service name")
        return ",".join(names)

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        return value.upper()

    @model_validator(mode="after")
    def validate_burst_sizes(self) -> "Settings":
        if self.burst_max_size < self.burst_min_size:
            raise ValueError("BURST_MAX_SIZE must be greater than or equal to BURST_MIN_SIZE")
        return self

    @property
    def service_name_list(self) -> list[str]:
        return [item.strip() for item in self.service_names.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()

