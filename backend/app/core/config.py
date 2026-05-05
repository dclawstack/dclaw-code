"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """DClaw Code application settings."""

    app_env: str = "dev"
    log_level: str = "INFO"
    api_host: str = "0.0.0.0"
    api_port: int = 8094
    database_url: str = (
        "postgresql+asyncpg://postgres:postgres@localhost:5432/dclaw_code"
    )
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "codellama:7b-code"
    default_llm: str = "codellama"
    openrouter_api_key: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
