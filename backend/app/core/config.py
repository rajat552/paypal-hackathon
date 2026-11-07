
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
    DATABASE_URL: str = "sqlite+aiosqlite:///./paymesh.db"

    # PayPal Developer Sandbox
    PAYPAL_ENVIRONMENT: str = "sandbox"
    PAYPAL_CLIENT_ID: str = "sandbox_client_id_placeholder"
    PAYPAL_CLIENT_SECRET: str = "sandbox_client_secret_placeholder"
    PAYPAL_WEBHOOK_ID: str | None = None

    # AI Provider
    AI_PROVIDER: str = "gemini"
    AI_API_KEY: str | None = None
    AI_MODEL: str = "gemini-2.5-flash"

    # Channel3 Data
    CHANNEL3_API_KEY: str | None = None
    DEMO_DATA_MODE: str = "live_or_fixture"

    # MongoDB Atlas & AI
    MONGODB_URI: str | None = None
    MONGODB_AI_ENDPOINT: str = "https://ai.mongodb.com"
    MONGODB_MODEL_API_KEY: str | None = None

    @property
    def is_sqlite(self) -> bool:
        return self.DATABASE_URL.startswith("sqlite")

    @property
    def async_database_url(self) -> str:
        """Normalize DATABASE_URL for SQLAlchemy 2.0 AsyncEngine."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://") and "+asyncpg" not in url:
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        elif url.startswith("sqlite://") and "+aiosqlite" not in url:
            url = url.replace("sqlite://", "sqlite+aiosqlite://", 1)
        return url

    @property
    def sync_database_url(self) -> str:
        """Normalize DATABASE_URL for sync drivers (Alembic / psycopg2)."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
        elif url.startswith("postgresql+asyncpg://"):
            url = url.replace("postgresql+asyncpg://", "postgresql://", 1)
        elif url.startswith("sqlite+aiosqlite://"):
            url = url.replace("sqlite+aiosqlite://", "sqlite://", 1)
        return url

    @property
    def paypal_base_url(self) -> str:
        if self.PAYPAL_ENVIRONMENT.lower() == "production":
            return "https://api-m.paypal.com"
        return "https://api-m.sandbox.paypal.com"

settings = Settings()

