import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env", env_ignore_empty=True, extra="ignore"
    )

    DATABASE_URL: str
    SECRET_KEY: str = secrets.token_urlsafe(32)
    API_V1_STR: str = "/api/v1"
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_PASSWORD: str
    EMAIL_TEST_USER: str = "test.user@gmail.com"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    PROJECT_NAME: str = "Async FastAPI SQLAlchemy Project"
    LOG_LEVEL: str = "DEBUG"


settings = Settings()  # type: ignore
