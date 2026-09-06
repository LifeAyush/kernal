"""Provider-agnostic LLM interface. Default implementation is Sarvam 105B."""

import os
from pathlib import Path

from sarvamai import SarvamAI
from sarvamai.types.create_chat_completion_response import CreateChatCompletionResponse
from sarvamai.types.sarvam_model_ids import SarvamModelIds

_DEFAULT_MODEL: str = "sarvam-105b"
_REPO_ROOT: Path = Path(__file__).resolve().parents[4]
_ENV_FILES: tuple[Path, ...] = (
    Path("apps/api/.env"),
    Path(".env"),
    _REPO_ROOT / "apps/api/.env",
    _REPO_ROOT / ".env",
)


class LlmUnavailable(Exception):
    """Raised when the LLM is not configured or returns no text."""


def _env_file_value(path: Path, key: str) -> str | None:
    if not path.is_file():
        return None
    line: str
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped: str = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        name: str
        raw: str
        name, raw = stripped.split("=", 1)
        if name.strip() != key:
            continue
        value: str = raw.strip().strip("'").strip('"')
        if value:
            return value
    return None


def _env_value(key: str) -> str | None:
    env_value: str | None = os.environ.get(key)
    if env_value:
        return env_value
    path: Path
    for path in _ENV_FILES:
        file_value: str | None = _env_file_value(path, key)
        if file_value:
            return file_value
    return None


def complete(prompt: str) -> str:
    key: str | None = _env_value("SARVAM_API_KEY")
    if key is None:
        raise LlmUnavailable("SARVAM_API_KEY is not set")
    model: SarvamModelIds = _env_value("LLM_MODEL") or _DEFAULT_MODEL
    client: SarvamAI = SarvamAI(api_subscription_key=key)
    response: CreateChatCompletionResponse = client.chat.completions(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        reasoning_effort=None,
    )
    if not response.choices:
        raise LlmUnavailable("Sarvam returned no choices")
    content: str | None = response.choices[0].message.content
    if content is None or not content.strip():
        raise LlmUnavailable("Sarvam returned an empty completion")
    return content
