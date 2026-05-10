"""Google Cloud Text-to-Speech provider.

Uses the public REST endpoint via google-auth + requests so we do not
require the heavyweight google-cloud-texttospeech SDK to be installed.
The service account credentials are read from
``GOOGLE_APPLICATION_CREDENTIALS`` (path to a JSON key file).
"""

import base64
import logging
import os

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from .base import (
    PROVIDER_GOOGLE,
    TTSAPIError,
    TTSConfigurationError,
    TTSQuotaExceeded,
)


logger = logging.getLogger(__name__)


GOOGLE_TTS_ENDPOINT = 'https://texttospeech.googleapis.com/v1/text:synthesize'
GOOGLE_TTS_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'
GOOGLE_TTS_QUOTA_CACHE_PREFIX = 'reel_tts_google_quota_v1'
GOOGLE_TTS_QUOTA_CACHE_TIMEOUT_SECONDS = 60 * 60 * 24 * 45


GOOGLE_TTS_FREE_TIER_LIMITS = {
    'standard': 4_000_000,
    'wavenet': 4_000_000,
    'neural2': 1_000_000,
    'studio': 1_000_000,
    'chirp3-hd': 1_000_000,
}

GOOGLE_TTS_EFFECTS_PROFILE_IDS = {
    '',
    'wearable-class-device',
    'handset-class-device',
    'headphone-class-device',
    'small-bluetooth-speaker-class-device',
    'medium-bluetooth-speaker-class-device',
    'large-home-entertainment-class-device',
    'large-automotive-class-device',
    'telephony-class-application',
}


_CHIRP3_HD_VOICES = [
    ('Achernar', 'FEMALE'),
    ('Achird', 'MALE'),
    ('Algenib', 'MALE'),
    ('Algieba', 'MALE'),
    ('Alnilam', 'MALE'),
    ('Aoede', 'FEMALE'),
    ('Autonoe', 'FEMALE'),
    ('Callirrhoe', 'FEMALE'),
    ('Charon', 'MALE'),
    ('Despina', 'FEMALE'),
    ('Enceladus', 'MALE'),
    ('Erinome', 'FEMALE'),
    ('Fenrir', 'MALE'),
    ('Gacrux', 'FEMALE'),
    ('Iapetus', 'MALE'),
    ('Kore', 'FEMALE'),
    ('Laomedeia', 'FEMALE'),
    ('Leda', 'FEMALE'),
    ('Orus', 'MALE'),
    ('Puck', 'MALE'),
    ('Pulcherrima', 'FEMALE'),
    ('Rasalgethi', 'MALE'),
    ('Sadachbia', 'MALE'),
    ('Sadaltager', 'MALE'),
    ('Schedar', 'MALE'),
    ('Sulafat', 'FEMALE'),
    ('Umbriel', 'MALE'),
    ('Vindemiatrix', 'FEMALE'),
    ('Zephyr', 'FEMALE'),
    ('Zubenelgenubi', 'MALE'),
]


DEFAULT_FRENCH_VOICES = [
    {
        'voice_id': 'fr-FR-Standard-F',
        'name': 'Standard F (feminine - 4M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'FEMALE',
        'tier': 'standard',
    },
    {
        'voice_id': 'fr-FR-Standard-G',
        'name': 'Standard G (masculine - 4M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'MALE',
        'tier': 'standard',
    },
    {
        'voice_id': 'fr-FR-Wavenet-F',
        'name': 'Wavenet F (feminine - 4M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'FEMALE',
        'tier': 'wavenet',
    },
    {
        'voice_id': 'fr-FR-Wavenet-G',
        'name': 'Wavenet G (masculine - 4M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'MALE',
        'tier': 'wavenet',
    },
    {
        'voice_id': 'fr-FR-Neural2-F',
        'name': 'Neural2 F (feminine - 1M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'FEMALE',
        'tier': 'neural2',
    },
    {
        'voice_id': 'fr-FR-Neural2-G',
        'name': 'Neural2 G (masculine - 1M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'MALE',
        'tier': 'neural2',
    },
    {
        'voice_id': 'fr-FR-Studio-A',
        'name': 'Studio A (feminine - 1M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'FEMALE',
        'tier': 'studio',
    },
    {
        'voice_id': 'fr-FR-Studio-D',
        'name': 'Studio D (masculine - 1M free chars/month)',
        'language_code': 'fr-FR',
        'gender': 'MALE',
        'tier': 'studio',
    },
] + [
    {
        'voice_id': f'fr-FR-Chirp3-HD-{name}',
        'name': f'{name} (Chirp3 HD - 1M free chars/month)',
        'language_code': 'fr-FR',
        'gender': gender,
        'tier': 'chirp3-hd',
    }
    for name, gender in _CHIRP3_HD_VOICES
]


def _allowed_voice_ids():
    return {voice['voice_id'] for voice in DEFAULT_FRENCH_VOICES}


def _quota_disable_ratio():
    try:
        ratio = float(getattr(settings, 'GOOGLE_TTS_QUOTA_DISABLE_RATIO', 0.90) or 0.90)
    except (TypeError, ValueError):
        ratio = 0.90
    return min(max(ratio, 0.0), 1.0)


def _quota_month():
    return timezone.now().strftime('%Y-%m')


def _quota_cache_key(tier):
    return f'{GOOGLE_TTS_QUOTA_CACHE_PREFIX}:{_quota_month()}:{tier}'


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _optional_float(value, *, minimum, maximum):
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return min(max(number, minimum), maximum)


def _tier_free_limit(tier):
    return GOOGLE_TTS_FREE_TIER_LIMITS.get(str(tier or '').strip().lower(), 0)


def _quota_used_characters(tier):
    return max(_safe_int(cache.get(_quota_cache_key(tier)), 0), 0)


def _quota_snapshot_for_tier(tier):
    safe_tier = str(tier or '').strip().lower()
    limit = _tier_free_limit(safe_tier)
    used = _quota_used_characters(safe_tier)
    disable_ratio = _quota_disable_ratio()
    disable_at = int(limit * disable_ratio) if limit else 0
    used_ratio = (used / limit) if limit else 0.0
    disabled = bool(limit and used >= disable_at)

    if disabled:
        status = 'disabled'
    elif limit and used >= int(limit * 0.80):
        status = 'near_limit'
    else:
        status = 'ok'

    return {
        'month': _quota_month(),
        'bucket': safe_tier,
        'used_characters': used,
        'free_monthly_character_limit': limit,
        'disable_at_characters': disable_at,
        'disable_ratio': disable_ratio,
        'used_ratio': round(used_ratio, 6),
        'used_percent': round(used_ratio * 100, 2),
        'remaining_free_characters': max(limit - used, 0) if limit else 0,
        'remaining_until_disable_characters': max(disable_at - used, 0) if limit else 0,
        'status': status,
        'disabled': disabled,
    }


def quota_snapshot_for_voice(voice_id):
    voice_meta = _voice_metadata(str(voice_id or '').strip())
    return _quota_snapshot_for_tier(voice_meta.get('tier'))


def _apply_quota_metadata(voice):
    quota = _quota_snapshot_for_tier(voice.get('tier'))
    item = dict(voice)
    item['quota'] = quota
    item['quota_bucket'] = quota['bucket']
    item['quota_used_characters'] = quota['used_characters']
    item['quota_used_ratio'] = quota['used_ratio']
    item['quota_used_percent'] = quota['used_percent']
    item['free_monthly_character_limit'] = quota['free_monthly_character_limit']
    item['quota_disable_at_characters'] = quota['disable_at_characters']
    item['quota_disable_ratio'] = quota['disable_ratio']
    item['quota_remaining_until_disable_characters'] = quota['remaining_until_disable_characters']
    item['quota_status'] = quota['status']
    item['api_usable'] = not quota['disabled']
    if quota['disabled']:
        item['api_usable_reason'] = (
            f"Quota local Google {quota['bucket']} a {quota['used_percent']}% "
            f"(seuil {int(quota['disable_ratio'] * 100)}%)."
        )
    return item


def assert_quota_available(voice_id, character_count):
    quota = quota_snapshot_for_voice(voice_id)
    if not quota['free_monthly_character_limit']:
        return

    safe_count = max(_safe_int(character_count), 0)
    projected = quota['used_characters'] + safe_count
    if projected <= quota['disable_at_characters']:
        return

    raise TTSQuotaExceeded(
        'Quota gratuit Google TTS presque atteint pour '
        f"{quota['bucket']} ({quota['used_characters']:,}/"
        f"{quota['free_monthly_character_limit']:,} caracteres utilises, "
        f"seuil {int(quota['disable_ratio'] * 100)}%). "
        'Choisis une autre famille de voix ou attends le mois prochain.'
    )


def record_quota_usage(voice_id, character_count):
    voice_meta = _voice_metadata(str(voice_id or '').strip())
    tier = str(voice_meta.get('tier') or '').strip().lower()
    if not _tier_free_limit(tier):
        return quota_snapshot_for_voice(voice_id)

    key = _quota_cache_key(tier)
    used = _quota_used_characters(tier)
    used += max(_safe_int(character_count), 0)
    cache.set(key, used, timeout=GOOGLE_TTS_QUOTA_CACHE_TIMEOUT_SECONDS)
    return quota_snapshot_for_voice(voice_id)


def get_default_voice_id():
    configured = str(getattr(settings, 'GOOGLE_TTS_DEFAULT_VOICE', '') or '').strip()
    if configured in _allowed_voice_ids():
        return configured
    if configured:
        logger.warning(
            'Ignoring GOOGLE_TTS_DEFAULT_VOICE=%s because it is not in the Reel Studio Google voice allow-list.',
            configured,
        )
    return DEFAULT_FRENCH_VOICES[0]['voice_id']


def get_default_language_code():
    return str(getattr(settings, 'GOOGLE_TTS_DEFAULT_LANGUAGE', 'fr-FR') or 'fr-FR').strip()


def list_voices():
    """Return the static list of supported French voices, with the configured default first."""
    default_voice_id = get_default_voice_id()
    voices = []
    for voice in DEFAULT_FRENCH_VOICES:
        item = _apply_quota_metadata(voice)
        item['provider'] = PROVIDER_GOOGLE
        item['is_default'] = (item['voice_id'] == default_voice_id)
        voices.append(item)

    voices.sort(key=lambda item: (
        not item.get('is_default'),
        item.get('api_usable') is False,
        item.get('tier') != 'standard',
        item.get('tier') != 'wavenet',
        item.get('tier') != 'chirp3-hd',
        item.get('name') or '',
    ))
    return voices


def _credentials_path():
    path = str(getattr(settings, 'GOOGLE_APPLICATION_CREDENTIALS', '') or '').strip()
    if not path:
        path = str(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS') or '').strip()
    if not path:
        return ''
    path = os.path.expandvars(os.path.expanduser(path))
    if os.path.isabs(path):
        return path

    base_dir = getattr(settings, 'BASE_DIR', '')
    if base_dir:
        return os.path.abspath(os.path.join(str(base_dir), path))
    return path


def _get_access_token():
    path = _credentials_path()
    if not path:
        raise TTSConfigurationError(
            'GOOGLE_APPLICATION_CREDENTIALS non configure (chemin vers le JSON service account).'
        )
    if not os.path.exists(path):
        raise TTSConfigurationError(
            f'Fichier credentials Google introuvable: {path}'
        )

    try:
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request as GoogleAuthRequest
    except ImportError as exc:
        raise TTSConfigurationError(
            "Le paquet 'google-auth' est requis pour Google TTS."
        ) from exc

    try:
        credentials = service_account.Credentials.from_service_account_file(
            path,
            scopes=[GOOGLE_TTS_SCOPE],
        )
        credentials.refresh(GoogleAuthRequest())
    except Exception as exc:
        raise TTSConfigurationError(
            f'Impossible de charger les credentials Google: {exc}'
        ) from exc

    token = getattr(credentials, 'token', '') or ''
    if not token:
        raise TTSConfigurationError('Google TTS: jeton OAuth vide.')
    return token


def _resolve_audio_encoding(output_format):
    fmt = str(output_format or 'mp3').strip().lower()
    if fmt in ('mp3', 'mp3_44100', 'mp3_44100_128', ''):
        return 'MP3'
    if fmt in ('ogg', 'ogg_opus'):
        return 'OGG_OPUS'
    if fmt in ('wav', 'linear16', 'pcm'):
        return 'LINEAR16'
    return 'MP3'


def build_generation_options(
    *,
    output_format='mp3',
    speaking_rate=None,
    pitch=None,
    volume_gain_db=None,
    effects_profile_id='',
):
    audio_config = {
        'audioEncoding': _resolve_audio_encoding(output_format),
    }

    normalized_speaking_rate = _optional_float(speaking_rate, minimum=0.25, maximum=4.0)
    if normalized_speaking_rate is not None:
        audio_config['speakingRate'] = normalized_speaking_rate

    normalized_pitch = _optional_float(pitch, minimum=-20.0, maximum=20.0)
    if normalized_pitch is not None:
        audio_config['pitch'] = normalized_pitch

    normalized_volume_gain = _optional_float(volume_gain_db, minimum=-96.0, maximum=16.0)
    if normalized_volume_gain is not None:
        audio_config['volumeGainDb'] = normalized_volume_gain

    normalized_profile = str(effects_profile_id or '').strip()
    if normalized_profile:
        if normalized_profile not in GOOGLE_TTS_EFFECTS_PROFILE_IDS:
            raise TTSConfigurationError(f"Profil audio Google TTS non autorise: '{normalized_profile}'.")
        audio_config['effectsProfileId'] = [normalized_profile]

    return audio_config


def _normalize_voice_id(voice_id):
    resolved = str(voice_id or '').strip() or get_default_voice_id()
    if resolved not in _allowed_voice_ids():
        allowed = ', '.join(sorted(_allowed_voice_ids()))
        raise TTSConfigurationError(
            f"Voix Google TTS non autorisee: '{resolved}'. "
            f"Voix Google gratuites activees dans Reel Studio: {allowed}."
        )
    return resolved


def _voice_metadata(voice_id):
    for voice in DEFAULT_FRENCH_VOICES:
        if voice['voice_id'] == voice_id:
            return voice
    return {
        'voice_id': voice_id,
        'language_code': get_default_language_code(),
        'gender': 'NEUTRAL',
    }


def _max_text_chars():
    try:
        return int(getattr(settings, 'GOOGLE_TTS_MAX_TEXT_CHARS', 4500) or 4500)
    except (TypeError, ValueError):
        return 4500


def synthesize(
    *,
    text,
    voice_id='',
    model_id='',
    output_format='mp3',
    speaking_rate=None,
    pitch=None,
    volume_gain_db=None,
    effects_profile_id='',
):
    """Generate MP3 bytes via Google Cloud TTS.

    Returns a dict matching ``TTSResult`` fields (audio_bytes, voice_id, ...).
    Raises ``ValueError`` for empty/oversized text, ``TTSConfigurationError`` for
    missing credentials, and ``TTSAPIError`` for transport/API failures.
    """
    safe_text = str(text or '').strip()
    if not safe_text:
        raise ValueError('Aucun texte voix a generer.')

    max_chars = _max_text_chars()
    if len(safe_text) > max_chars:
        raise ValueError(
            f'Texte voix trop long pour Google TTS ({len(safe_text)}/{max_chars} caracteres).'
        )

    resolved_voice_id = _normalize_voice_id(voice_id)
    assert_quota_available(resolved_voice_id, len(safe_text))
    voice_meta = _voice_metadata(resolved_voice_id)
    language_code = voice_meta.get('language_code') or get_default_language_code()
    audio_config = build_generation_options(
        output_format=output_format,
        speaking_rate=speaking_rate,
        pitch=pitch,
        volume_gain_db=volume_gain_db,
        effects_profile_id=effects_profile_id,
    )
    audio_encoding = audio_config['audioEncoding']

    try:
        token = _get_access_token()
    except TTSConfigurationError:
        raise

    payload = {
        'input': {'text': safe_text},
        'voice': {
            'languageCode': language_code,
            'name': resolved_voice_id,
        },
        'audioConfig': audio_config,
    }

    timeout = float(getattr(settings, 'GOOGLE_TTS_TIMEOUT_SECONDS', 60) or 60)

    try:
        response = requests.post(
            GOOGLE_TTS_ENDPOINT,
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json; charset=utf-8',
            },
            json=payload,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise TTSAPIError('Timeout Google TTS pendant la generation audio.') from exc
    except requests.RequestException as exc:
        raise TTSAPIError('Erreur reseau Google TTS pendant la generation audio.') from exc

    if response.status_code >= 400:
        try:
            payload = response.json()
            err = payload.get('error') or {}
            detail = err.get('message') or response.reason or 'Google TTS a echoue.'
        except ValueError:
            detail = response.text[:500] or response.reason or 'Google TTS a echoue.'
        raise TTSAPIError(f'Google TTS HTTP {response.status_code}: {detail}')

    try:
        body = response.json()
    except ValueError as exc:
        raise TTSAPIError('Reponse Google TTS illisible.') from exc

    audio_b64 = body.get('audioContent') or ''
    if not audio_b64:
        raise TTSAPIError('Google TTS a retourne un audio vide.')

    try:
        audio_bytes = base64.b64decode(audio_b64)
    except Exception as exc:
        raise TTSAPIError('Audio Google TTS invalide.') from exc

    quota = record_quota_usage(resolved_voice_id, len(safe_text))

    return {
        'audio_bytes': audio_bytes,
        'voice_id': resolved_voice_id,
        'model_id': resolved_voice_id,
        'output_format': 'mp3' if audio_encoding == 'MP3' else audio_encoding.lower(),
        'language_code': language_code,
        'character_count': len(safe_text),
        'quota': quota,
    }
