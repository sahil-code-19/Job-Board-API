from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url : str
    redis_url : str = "redis://redis:6379"
    secret_key : str
    algorithm : str = "HS256"
    access_token_expire_minutes : int = 30
    refresh_token_expire_days : int = 7
    resend_api_key : str
    cors_origins : str = "*"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()