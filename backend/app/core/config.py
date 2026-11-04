
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", "../.env", "server/.env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    APP_ENV: str = "development"
    APP_BASE_URL: str = "http://localhost:8000"
    FRONTEND_URL: str = "http://localhost:3000"
    SECRET_KEY: str = "paymesh-ai-default-secret-key-min-32-chars-long"
    ACCESS_TOKEN_TTL_MINUTES: int = 60
    PAYMENT_CHALLENGE_TTL_MINUTES: int = 10
    LOG_LEVEL: str = "INFO"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./crawlerpal.db"

    # PayPal Developer Sandbox
    PAYPAL_ENVIRONMENT: str = "sandbox"
    PAYPAL_CLIENT_ID: str = "sandbox_client_id_placeholder"
    PAYPAL_CLIENT_SECRET: str = "sandbox_client_secret_placeholder"
    PAYPAL_WEBHOOK_ID: str | None = None

    # AI Provider
    AI_PROVIDER: str = "openai"
    AI_API_KEY: str | None = None
    AI_MODEL: str = "gpt-4o-mini"

    # Channel3 Data
    CHANNEL3_API_KEY: str | None = None
    DEMO_DATA_MODE: str = "live_or_fixture"

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

    @property
    def sync_database_url(self) -> str:
        if self.DATABASE_URL.startswith("sqlite+aiosqlite://"):
            return self.DATABASE_URL.replace("sqlite+aiosqlite://", "sqlite://")
        if self.DATABASE_URL.startswith("postgresql+psycopg://"):
            return self.DATABASE_URL.replace("postgresql+psycopg://", "postgresql://")
        return self.DATABASE_URL

    @property
    def paypal_base_url(self) -> str:
        if self.PAYPAL_ENVIRONMENT.lower() == "production":
            return "https://api-m.paypal.com"
        return "https://api-m.sandbox.paypal.com"

settings = Settings()

