"""Generic TTS dispatch layer.

This package provides a single entry point that routes speech generation
to one of several providers (Google Cloud TTS by default, ElevenLabs as a
premium option). Each provider lives in its own module and exposes a
common interface so the rest of the app does not have to care about the
underlying API.
"""

from .base import (
    PROVIDER_ELEVENLABS,
    PROVIDER_GOOGLE,
    SUPPORTED_PROVIDERS,
    TTSAPIError,
    TTSConfigurationError,
    TTSQuotaExceeded,
    TTSResult,
)
from .dispatch import (
    generate_speech,
    list_provider_voices,
    list_providers_payload,
    resolve_default_voice,
)

__all__ = [
    'PROVIDER_ELEVENLABS',
    'PROVIDER_GOOGLE',
    'SUPPORTED_PROVIDERS',
    'TTSAPIError',
    'TTSConfigurationError',
    'TTSQuotaExceeded',
    'TTSResult',
    'generate_speech',
    'list_provider_voices',
    'list_providers_payload',
    'resolve_default_voice',
]
