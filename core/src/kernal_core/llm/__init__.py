"""Provider-agnostic LLM interface. Default implementation is Sarvam 105B."""

from sarvamai import SarvamAI
from sarvamai.types.create_chat_completion_response import CreateChatCompletionResponse
from sarvamai.types.sarvam_model_ids import SarvamModelIds

from kernal_core.settings import settings

_DEFAULT_MODEL: str = "sarvam-105b"


class LlmUnavailable(Exception):
    """Raised when the LLM is not configured or returns no text."""


def complete(prompt: str) -> str:
    key: str | None = settings.sarvam_api_key
    if key is None:
        raise LlmUnavailable("SARVAM_API_KEY is not set")
    model: SarvamModelIds = settings.llm_model or _DEFAULT_MODEL
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
