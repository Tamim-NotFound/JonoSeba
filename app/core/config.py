from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "JonoSeba API"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = (
        "AI-Powered Smart Citizen Services "
        "and Complaint Management Platform."
    )

    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # PostgreSQL
    DATABASE_URL: str

    # JWT Authentication
    JWT_SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        gt=0,
    )

    # Google Gemini AI
    GEMINI_API_KEY: str | None = None
    GEMINI_MODEL: str = "gemini-3.1-flash-lite"
    GEMINI_TEMPERATURE: float = Field(
        default=0.3,
        ge=0,
        le=2,
    )
    GEMINI_MAX_OUTPUT_TOKENS: int = Field(
        default=800,
        gt=0,
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
