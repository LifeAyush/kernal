from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

_REPO_ROOT: Path = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            Path(".env"),
            Path("apps/api/.env"),
            _REPO_ROOT / ".env",
            _REPO_ROOT / "apps/api/.env",
        ),
        extra="ignore",
    )

    database_url: str | None = None
    sarvam_api_key: str | None = None
    llm_model: str | None = None

    @field_validator("database_url", "sarvam_api_key", "llm_model", mode="before")
    @classmethod
    def _empty_as_unset(cls, value: object) -> str | None:
        if value is None:
            return None
        text: str = str(value).strip()
        if text == "":
            return None
        return text


settings: Settings = Settings()
