"""Shared types and exceptions for the TTS dispatcher."""

from dataclasses import dataclass, field


PROVIDER_GOOGLE = 'google'
PROVIDER_ELEVENLABS = 'elevenlabs'
SUPPORTED_PROVIDERS = (PROVIDER_GOOGLE, PROVIDER_ELEVENLABS)


class TTSConfigurationError(Exception):
    """Raised when a provider is missing API keys, credentials, or settings."""


class TTSAPIError(Exception):
    """Raised when a provider's HTTP/SDK call fails at runtime."""


class TTSQuotaExceeded(Exception):
    """Raised when a provider quota guard blocks a new upstream call."""


@dataclass
class TTSResult:
    audio_bytes: bytes
    provider: str
    voice_id: str
    model_id: str = ''
    output_format: str = 'mp3'
    character_count: int = 0
    cached: bool = False
    cache_key: str = ''
    extra: dict = field(default_factory=dict)

    def as_legacy_dict(self):
        """Backwards-compat shape used by the historical ElevenLabs code path."""
        return {
            'audio_bytes': self.audio_bytes,
            'voice_id': self.voice_id,
            'model_id': self.model_id,
            'output_format': self.output_format,
            'provider': self.provider,
            'character_count': self.character_count,
            'cached': self.cached,
            'cache_key': self.cache_key,
        }
