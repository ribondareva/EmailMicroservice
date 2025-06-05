from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # PostgreSQL
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str
    postgres_port: int
    database_url: str  # Можно использовать для asyncpg / SQLAlchemy

    # SMTP
    smtp_host: str
    smtp_port: int
    smtp_user: str | None = None  # обычно MailHog не требует
    smtp_password: str | None = None
    sender_email: EmailStr

    # IMAP
    imap_host: str
    imap_port: int
    imap_user: str | None = None
    imap_password: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
