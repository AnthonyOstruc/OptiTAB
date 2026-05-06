"""TTS dispatcher: routes a generic synthesis request to the right provider.

Adds a thin caching layer (Django cache + storage backend) so that the same
``provider + voice + text`` triplet does not hit the upstream API twice.
"""

import hashlib
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .base import (
    PROVIDER_ELEVENLABS,
    PROVIDER_GOOGLE,
    SUPPORTED_PROVIDERS,
    TTSAPIError,
    TTSConfigurationError,
    TTSResult,
)
from . import google as google_provider


logger = logging.getLogger(__name__)


CACHE_PREFIX = 'reel_tts_cache_v1'
CACHE_STORAGE_FOLDER = 'reel_studio/tts_cache'


def _normalize_provider(provider):
    raw = str(provider or '').strip().lower()
    if not raw:
        return get_default_provider()
    if raw in SUPPORTED_PROVIDERS:
        return raw
    aliases = {
        'gcloud': PROVIDER_GOOGLE,
        'google_tts': PROVIDER_GOOGLE,
        'eleven': PROVIDER_ELEVENLABS,
        'elevenlabs_v2': PROVIDER_ELEVENLABS,
    }
    if raw in aliases:
        return aliases[raw]
    raise TTSConfigurationError(f"Fournisseur TTS inconnu: '{provider}'.")


def get_default_provider():
    raw = str(getattr(settings, 'REEL_TTS_DEFAULT_PROVIDER', PROVIDER_GOOGLE) or PROVIDER_GOOGLE).strip().lower()
    return raw if raw in SUPPORTED_PROVIDERS else PROVIDER_GOOGLE


def _hash_text(text):
    digest = hashlib.sha256(str(text or '').encode('utf-8')).hexdigest()
    return digest[:48]


def _cache_key(provider, voice_id, text):
    return f'{CACHE_PREFIX}:{provider}:{voice_id}:{_hash_text(text)}'


def _cache_storage_path(provider, voice_id, text):
    return f'{CACHE_STORAGE_FOLDER}/{provider}/{voice_id}/{_hash_text(text)}.mp3'


def _read_cached_audio(provider, voice_id, text):
    """Look up a previously generated MP3 for the same (provider, voice, text)."""
    key = _cache_key(provider, voice_id, text)
    storage_path = cache.get(key)

    if not storage_path:
        # Fallback: probe storage directly so cache evictions do not force regeneration.
        candidate = _cache_storage_path(provider, voice_id, text)
        if default_storage.exists(candidate):
            storage_path = candidate
            try:
                cache.set(key, candidate, timeout=60 * 60 * 24 * 30)
            except Exception:
                pass

    if not storage_path:
        return None, key

    try:
        with default_storage.open(storage_path, 'rb') as handle:
            return handle.read(), key
    except Exception as exc:
        logger.warning('TTS cache miss (storage read failed) for %s: %s', storage_path, exc)
        try:
            cache.delete(key)
        except Exception:
            pass
        return None, key


def _store_cached_audio(provider, voice_id, text, audio_bytes):
    if not audio_bytes:
        return ''
    storage_path = _cache_storage_path(provider, voice_id, text)
    try:
        if default_storage.exists(storage_path):
            default_storage.delete(storage_path)
    except Exception:
        pass

    try:
        default_storage.save(storage_path, ContentFile(audio_bytes))
    except Exception as exc:
        logger.warning('TTS cache write failed for %s: %s', storage_path, exc)
        return ''

    try:
        cache.set(_cache_key(provider, voice_id, text), storage_path, timeout=60 * 60 * 24 * 30)
    except Exception:
        pass

    return storage_path


def resolve_default_voice(provider):
    provider = _normalize_provider(provider)
    if provider == PROVIDER_GOOGLE:
        return google_provider.get_default_voice_id()
    return str(getattr(settings, 'ELEVENLABS_VOICE_ID', '') or '').strip()


def list_provider_voices(provider):
    provider = _normalize_provider(provider)
    if provider == PROVIDER_GOOGLE:
        return google_provider.list_voices()

    # ElevenLabs: reuse the existing helper to keep the legacy filter behaviour.
    from ..elevenlabs import list_filtered_voices, ElevenLabsAPIError, ElevenLabsConfigurationError

    try:
        voices = list_filtered_voices(language='fr', accent='parisian', include_fallback=True)
    except ElevenLabsConfigurationError as exc:
        raise TTSConfigurationError(str(exc)) from exc
    except ElevenLabsAPIError as exc:
        raise TTSAPIError(str(exc)) from exc

    for voice in voices:
        voice['provider'] = PROVIDER_ELEVENLABS
    return voices


def _provider_usage(provider):
    if provider != PROVIDER_ELEVENLABS:
        return None

    from ..elevenlabs import (
        ElevenLabsAPIError,
        ElevenLabsConfigurationError,
        get_subscription_usage,
    )

    try:
        return get_subscription_usage()
    except ElevenLabsConfigurationError as exc:
        return {
            'available': False,
            'error_code': 'not_configured',
            'error': str(exc),
        }
    except ElevenLabsAPIError as exc:
        error = str(exc)
        error_code = 'missing_permissions' if 'missing_permissions' in error else 'api_error'
        return {
            'available': False,
            'error_code': error_code,
            'error': error,
        }


def list_providers_payload():
    """Aggregate provider+voice info for the frontend dropdowns."""
    default_provider = get_default_provider()
    payload = {
        'default_provider': default_provider,
        'providers': [],
    }

    for provider in SUPPORTED_PROVIDERS:
        item = {
            'id': provider,
            'label': _provider_label(provider),
            'is_default': provider == default_provider,
            'configured': _provider_is_configured(provider),
            'default_voice_id': '',
            'voices': [],
            'usage': None,
            'error': '',
        }
        try:
            item['default_voice_id'] = resolve_default_voice(provider)
            item['voices'] = list_provider_voices(provider)
            item['usage'] = _provider_usage(provider)
        except TTSConfigurationError as exc:
            item['error'] = str(exc)
        except TTSAPIError as exc:
            item['error'] = str(exc)
        except Exception as exc:  # defensive: never let one provider break the list
            item['error'] = f'{type(exc).__name__}: {exc}'
        payload['providers'].append(item)

    return payload


def _provider_label(provider):
    if provider == PROVIDER_GOOGLE:
        return 'Google Cloud Text-to-Speech (quota gratuit)'
    if provider == PROVIDER_ELEVENLABS:
        return 'ElevenLabs'
    return provider


def _provider_is_configured(provider):
    if provider == PROVIDER_GOOGLE:
        path = str(getattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS', '') or '').strip()
        if not path:
            import os
            path = str(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or '').strip()
        return bool(path)
    if provider == PROVIDER_ELEVENLABS:
        return bool(str(getattr(settings, 'ELEVENLABS_API_KEY', '') or '').strip())
    return False


def generate_speech(*, text, provider='', voice_id='', model_id='', output_format='', use_cache=True):
    """Top-level entry point used by the views.

    - Validates provider/voice
    - Looks up the cache (provider+voice+text)
    - Falls back to upstream API if no cache hit
    - Stores the result in the cache
    - Returns a ``TTSResult``
    """
    safe_text = str(text or '').strip()
    if not safe_text:
        raise ValueError('Aucun texte voix a generer.')

    resolved_provider = _normalize_provider(provider)
    resolved_voice_id = (voice_id or '').strip() or resolve_default_voice(resolved_provider)
    if not resolved_voice_id:
        raise TTSConfigurationError(f"Aucune voix configuree pour le provider '{resolved_provider}'.")

    if use_cache:
        cached_bytes, cache_key = _read_cached_audio(resolved_provider, resolved_voice_id, safe_text)
        if cached_bytes:
            logger.info(
                'TTS cache hit | provider=%s | voice=%s | chars=%d',
                resolved_provider, resolved_voice_id, len(safe_text),
            )
            return TTSResult(
                audio_bytes=cached_bytes,
                provider=resolved_provider,
                voice_id=resolved_voice_id,
                model_id=model_id or resolved_voice_id,
                output_format=output_format or 'mp3',
                character_count=len(safe_text),
                cached=True,
                cache_key=cache_key,
            )
    else:
        cache_key = _cache_key(resolved_provider, resolved_voice_id, safe_text)

    # Cache miss -> call the provider.
    if resolved_provider == PROVIDER_GOOGLE:
        result = google_provider.synthesize(
            text=safe_text,
            voice_id=resolved_voice_id,
            model_id=model_id,
            output_format=output_format or 'mp3',
        )
    elif resolved_provider == PROVIDER_ELEVENLABS:
        from ..elevenlabs import (
            ElevenLabsAPIError,
            ElevenLabsConfigurationError,
            generate_speech_mp3,
        )
        try:
            result = generate_speech_mp3(
                text=safe_text,
                voice_id=resolved_voice_id,
                model_id=model_id,
                output_format=output_format,
            )
        except ElevenLabsConfigurationError as exc:
            raise TTSConfigurationError(str(exc)) from exc
        except ElevenLabsAPIError as exc:
            raise TTSAPIError(str(exc)) from exc
        # ElevenLabs result already has the right shape, just add character_count.
        result['character_count'] = len(safe_text)
    else:
        raise TTSConfigurationError(f"Provider TTS non supporte: '{resolved_provider}'.")

    audio_bytes = result.get('audio_bytes') or b''
    if not audio_bytes:
        raise TTSAPIError(f'{resolved_provider}: audio vide.')

    if use_cache:
        _store_cached_audio(resolved_provider, resolved_voice_id, safe_text, audio_bytes)

    logger.info(
        'TTS generate | provider=%s | voice=%s | chars=%d | bytes=%d | cached=%s',
        resolved_provider,
        resolved_voice_id,
        len(safe_text),
        len(audio_bytes),
        False,
    )

    return TTSResult(
        audio_bytes=audio_bytes,
        provider=resolved_provider,
        voice_id=result.get('voice_id') or resolved_voice_id,
        model_id=result.get('model_id') or model_id or resolved_voice_id,
        output_format=result.get('output_format') or output_format or 'mp3',
        character_count=len(safe_text),
        cached=False,
        cache_key=cache_key,
        extra={'language_code': result.get('language_code', '')},
    )
