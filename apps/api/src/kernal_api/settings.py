from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

_API_ROOT: Path = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(_API_ROOT / ".env", Path(".env")),
        extra="ignore",
    )

    cors_origins: str = "http://localhost:5173"
    database_url: str | None = None
    cron_secret: str | None = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings: Settings = Settings()
