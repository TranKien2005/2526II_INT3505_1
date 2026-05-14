from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Book Management Production API"
    app_env: str = "production"
    database_url: str = f"sqlite:///{BASE_DIR / 'books.db'}"
    api_key: str = "demo-secret-key"
    log_level: str = "INFO"
    rate_limit_default: str = "20/minute"
    rate_limit_book_create: str = "5/minute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
