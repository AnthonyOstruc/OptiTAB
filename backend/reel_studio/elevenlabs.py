import logging
import re

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


BUILTIN_EXTRA_VOICES = (
    {
        'name': 'Marine - Premium Conversational AI',
        'voice_id': '6FXyooAOTqUK8m2HWm32',
        'category': 'professional',
        'is_custom': False,
        'sort_priority': 0,
        'labels': {
            'language': 'fr',
            'accent': 'parisian',
            'gender': 'female',
        },
    },
    {
        'name': 'Nicolas',
        'voice_id': 'aQROLel5sQbj1vuIVi6B',
        'category': '',
        'is_custom': False,
        'sort_priority': 1,
        'labels': {
            'language': 'fr',
            'accent': 'parisian',
            'gender': 'male',
        },
    },
    {
        'name': 'Mylene',
        'voice_id': 'WQKwBV2Uzw1gSGr69N8I',
        'category': '',
        'is_custom': False,
        'sort_priority': 2,
        'labels': {
            'language': 'fr',
            'accent': 'parisian',
            'gender': 'female',
        },
    },
    {
        'name': 'Victoria',
        'voice_id': 'O31r762Gb3WFygrEOGh0',
        'category': '',
        'is_custom': False,
        'labels': {
            'language': 'fr',
            'accent': 'parisian',
            'gender': 'female',
        },
    },
)

MODEL_ID_ALIASES = {
    # The UI keeps the user-facing name requested for Reel Studio while the
    # ElevenLabs API currently exposes v3 as ``eleven_v3``.
    'eleven_multilingual_v3': 'eleven_v3',
}

TEXT_NORMALIZATION_MODES = {'auto', 'on', 'off'}


class ElevenLabsConfigurationError(Exception):
    pass


class ElevenLabsAPIError(Exception):
    pass


def _clean_speech_line(value):
    cleaned = str(value or '').replace('\r\n', '\n').replace('\r', '\n')
    lines = [re.sub(r'\s+', ' ', line).strip() for line in cleaned.split('\n')]
    return ' '.join(line for line in lines if line)


def _slide_speech_text(slide):
    voice_script = _clean_speech_line(getattr(slide, 'voice_script', ''))
    if voice_script:
        return voice_script

    fallback_parts = [
        _clean_speech_line(getattr(slide, 'title', '')),
        _clean_speech_line(getattr(slide, 'screen_text', '')),
    ]
    return '. '.join(part for part in fallback_parts if part)


def build_slide_speech_text(slide):
    return _slide_speech_text(slide).strip()


def build_project_speech_text(project):
    slides = list(project.slides.all().order_by('order', 'id'))
    parts = [_slide_speech_text(slide) for slide in slides]
    return '\n\n'.join(part for part in parts if part).strip()


def _extract_error_detail(response):
    try:
        payload = response.json()
    except ValueError:
        payload = {}

    detail = payload.get('detail') or payload.get('message') or payload.get('error')
    if isinstance(detail, dict):
        detail = detail.get('message') or detail.get('detail')
    if isinstance(detail, list):
        detail = ' '.join(str(item) for item in detail)

    return str(detail or response.reason or 'ElevenLabs request failed').strip()


def _extract_error_code(response):
    try:
        payload = response.json()
    except ValueError:
        return ''

    detail = payload.get('detail')
    if isinstance(detail, dict):
        return str(detail.get('status') or detail.get('code') or '').strip()
    return str(payload.get('status') or payload.get('code') or '').strip()


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _safe_float(value, default):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _safe_bool(value, default):
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {'1', 'true', 'yes', 'on'}:
        return True
    if normalized in {'0', 'false', 'no', 'off'}:
        return False
    return default


def _normalize_model_id(value):
    model_id = str(value or getattr(settings, 'ELEVENLABS_MODEL_ID', '') or '').strip()
    return MODEL_ID_ALIASES.get(model_id, model_id)


def _normalize_text_normalization(value):
    normalized = str(value or getattr(settings, 'ELEVENLABS_APPLY_TEXT_NORMALIZATION', 'on') or '').strip().lower()
    return normalized if normalized in TEXT_NORMALIZATION_MODES else 'on'


def build_generation_options(
    *,
    model_id='',
    output_format='',
    stability=None,
    similarity_boost=None,
    style=None,
    speed=None,
    use_speaker_boost=None,
    language_code='',
    apply_text_normalization='',
):
    return {
        'model_id': _normalize_model_id(model_id),
        'output_format': (
            output_format or getattr(settings, 'ELEVENLABS_OUTPUT_FORMAT', 'mp3_44100_128')
        ).strip(),
        'stability': _safe_float(
            stability,
            _safe_float(getattr(settings, 'ELEVENLABS_VOICE_STABILITY', 0.64), 0.64),
        ),
        'similarity_boost': _safe_float(
            similarity_boost,
            _safe_float(getattr(settings, 'ELEVENLABS_VOICE_SIMILARITY_BOOST', 0.84), 0.84),
        ),
        'style': _safe_float(
            style,
            _safe_float(getattr(settings, 'ELEVENLABS_VOICE_STYLE', 0.10), 0.10),
        ),
        'speed': _safe_float(
            speed,
            _safe_float(getattr(settings, 'ELEVENLABS_VOICE_SPEED', 1.0), 1.0),
        ),
        'use_speaker_boost': _safe_bool(
            use_speaker_boost,
            _safe_bool(getattr(settings, 'ELEVENLABS_USE_SPEAKER_BOOST', True), True),
        ),
        'language_code': str(
            language_code or getattr(settings, 'ELEVENLABS_LANGUAGE_CODE', 'fr') or ''
        ).strip(),
        'apply_text_normalization': _normalize_text_normalization(apply_text_normalization),
    }


def get_subscription_usage():
    api_key = getattr(settings, 'ELEVENLABS_API_KEY', '').strip()
    if not api_key:
        raise ElevenLabsConfigurationError('ELEVENLABS_API_KEY non configure.')

    try:
        response = requests.get(
            'https://api.elevenlabs.io/v1/user/subscription',
            headers={'xi-api-key': api_key},
            timeout=float(getattr(settings, 'ELEVENLABS_TIMEOUT_SECONDS', 60) or 60),
        )
    except requests.Timeout as exc:
        raise ElevenLabsAPIError('Timeout ElevenLabs pendant le chargement du quota.') from exc
    except requests.RequestException as exc:
        raise ElevenLabsAPIError('Erreur reseau ElevenLabs pendant le chargement du quota.') from exc

    if response.status_code >= 400:
        detail = _extract_error_detail(response)
        code = _extract_error_code(response)
        message = f'ElevenLabs HTTP {response.status_code}: {detail}'
        if code:
            message = f'{message} [{code}]'
        raise ElevenLabsAPIError(message)

    try:
        payload = response.json()
    except ValueError as exc:
        raise ElevenLabsAPIError('ElevenLabs a retourne un quota invalide.') from exc

    used = _safe_int(payload.get('character_count'))
    total = _safe_int(payload.get('character_limit'))
    remaining = max(total - used, 0) if total else 0
    used_percent = round((used / total) * 100, 2) if total else 0
    remaining_percent = round((remaining / total) * 100, 2) if total else 0

    return {
        'available': True,
        'tier': payload.get('tier') or '',
        'status': payload.get('status') or '',
        'used': used,
        'total': total,
        'remaining': remaining,
        'used_percent': used_percent,
        'remaining_percent': remaining_percent,
        'reset_unix': payload.get('next_character_count_reset_unix'),
        'currency': payload.get('currency') or '',
        'billing_period': payload.get('billing_period') or '',
        'character_refresh_period': payload.get('character_refresh_period') or '',
    }


def generate_speech_mp3(
    *,
    text,
    voice_id='',
    model_id='',
    output_format='',
    stability=None,
    similarity_boost=None,
    style=None,
    speed=None,
    use_speaker_boost=None,
    language_code='',
    apply_text_normalization='',
):
    api_key = getattr(settings, 'ELEVENLABS_API_KEY', '').strip()
    resolved_voice_id = (voice_id or getattr(settings, 'ELEVENLABS_VOICE_ID', '')).strip()
    options = build_generation_options(
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
        speed=speed,
        use_speaker_boost=use_speaker_boost,
        language_code=language_code,
        apply_text_normalization=apply_text_normalization,
    )
    resolved_model_id = options['model_id']
    resolved_output_format = options['output_format']
    max_chars = int(getattr(settings, 'ELEVENLABS_MAX_TEXT_CHARS', 10000) or 10000)

    safe_text = str(text or '').strip()
    if not safe_text:
        raise ValueError('Aucun texte voix a generer.')
    if len(safe_text) > max_chars:
        raise ValueError(f'Texte voix trop long ({len(safe_text)}/{max_chars} caracteres).')
    if not api_key:
        raise ElevenLabsConfigurationError('ELEVENLABS_API_KEY non configure.')
    if not resolved_voice_id:
        raise ElevenLabsConfigurationError('ELEVENLABS_VOICE_ID non configure.')

    api_url = getattr(settings, 'ELEVENLABS_API_URL', 'https://api.elevenlabs.io/v1/text-to-speech')
    timeout = float(getattr(settings, 'ELEVENLABS_TIMEOUT_SECONDS', 60) or 60)
    url = f'{api_url.rstrip("/")}/{resolved_voice_id}'

    payload = {
        'text': safe_text,
        'model_id': resolved_model_id,
        'voice_settings': {
            'stability': options['stability'],
            'similarity_boost': options['similarity_boost'],
            'style': options['style'],
            'speed': options['speed'],
            'use_speaker_boost': options['use_speaker_boost'],
        },
        'apply_text_normalization': options['apply_text_normalization'],
    }
    if options['language_code']:
        payload['language_code'] = options['language_code']

    try:
        response = requests.post(
            url,
            headers={
                'xi-api-key': api_key,
                'Content-Type': 'application/json',
                'Accept': 'audio/mpeg',
            },
            params={'output_format': resolved_output_format},
            json=payload,
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise ElevenLabsAPIError('Timeout ElevenLabs pendant la generation audio.') from exc
    except requests.RequestException as exc:
        raise ElevenLabsAPIError('Erreur reseau ElevenLabs pendant la generation audio.') from exc

    if response.status_code >= 400:
        detail = _extract_error_detail(response)
        raise ElevenLabsAPIError(f'ElevenLabs HTTP {response.status_code}: {detail}')

    audio_bytes = response.content or b''
    if not audio_bytes:
        raise ElevenLabsAPIError('ElevenLabs a retourne un fichier audio vide.')

    return {
        'audio_bytes': audio_bytes,
        'voice_id': resolved_voice_id,
        'model_id': resolved_model_id,
        'output_format': resolved_output_format,
    }


def force_align_speech(*, audio_bytes, text, audio_mime='audio/mpeg', audio_filename='audio.mp3'):
    """Aligne un fichier audio existant avec un texte connu via ElevenLabs.

    Renvoie un dict {'words': [{text, start, end}, ...], 'characters': [...]}
    ou un dict vide si l'API n'est pas accessible.
    """
    api_key = getattr(settings, 'ELEVENLABS_API_KEY', '').strip()
    if not api_key:
        raise ElevenLabsConfigurationError('ELEVENLABS_API_KEY non configure.')

    safe_text = str(text or '').strip()
    if not safe_text:
        raise ValueError('Aucun texte a aligner.')
    if not audio_bytes:
        raise ValueError('Aucun audio a aligner.')

    timeout = float(getattr(settings, 'ELEVENLABS_TIMEOUT_SECONDS', 60) or 60)
    url = 'https://api.elevenlabs.io/v1/forced-alignment'

    try:
        response = requests.post(
            url,
            headers={'xi-api-key': api_key},
            files={'file': (audio_filename, audio_bytes, audio_mime)},
            data={'text': safe_text},
            timeout=timeout,
        )
    except requests.Timeout as exc:
        raise ElevenLabsAPIError('Timeout ElevenLabs pendant l\'alignement audio.') from exc
    except requests.RequestException as exc:
        raise ElevenLabsAPIError('Erreur reseau ElevenLabs pendant l\'alignement audio.') from exc

    if response.status_code >= 400:
        detail = _extract_error_detail(response)
        raise ElevenLabsAPIError(f'ElevenLabs HTTP {response.status_code}: {detail}')

    try:
        payload = response.json()
    except ValueError as exc:
        raise ElevenLabsAPIError('ElevenLabs a retourne un alignement invalide.') from exc

    if not isinstance(payload, dict):
        return {'words': [], 'characters': []}

    raw_words = payload.get('words') if isinstance(payload.get('words'), list) else []
    raw_chars = payload.get('characters') if isinstance(payload.get('characters'), list) else []

    def _serialize_segment(item):
        if not isinstance(item, dict):
            return None
        text_value = item.get('text')
        if text_value is None:
            text_value = item.get('character') or item.get('word') or ''
        start = _safe_float(item.get('start'), -1)
        end = _safe_float(item.get('end'), -1)
        if start < 0 or end < 0:
            return None
        return {
            'text': str(text_value),
            'start': round(start, 3),
            'end': round(end, 3),
        }

    words = [seg for seg in (_serialize_segment(item) for item in raw_words) if seg]
    characters = [seg for seg in (_serialize_segment(item) for item in raw_chars) if seg]

    return {
        'words': words,
        'characters': characters,
        'loss': _safe_float(payload.get('loss'), 0.0),
    }


def _serialize_voice(voice, *, matches_filter):
    labels = voice.get('labels') or {}
    category = voice.get('category') or ''
    voice_language = str(labels.get('language') or '').strip().lower()
    voice_accent = str(labels.get('accent') or '').strip().lower()
    requires_subscription = category == 'professional'

    return {
        'voice_id': voice.get('voice_id') or '',
        'name': voice.get('name') or '',
        'category': category,
        'api_usable': True,
        'requires_subscription': requires_subscription,
        'matches_filter': bool(matches_filter),
        'preview_url': voice.get('preview_url') or '',
        'labels': {
            'language': voice_language,
            'accent': voice_accent,
            'gender': labels.get('gender') or '',
            'age': labels.get('age') or '',
            'descriptive': labels.get('descriptive') or '',
            'use_case': labels.get('use_case') or '',
        },
    }


def _first_verified_language_preview(voice, *, language='', accent=''):
    normalized_language = str(language or '').strip().lower()
    normalized_accent = str(accent or '').strip().lower()
    verified_languages = voice.get('verified_languages') or []
    if not isinstance(verified_languages, list):
        return ''

    fallback_preview = ''
    for item in verified_languages:
        if not isinstance(item, dict):
            continue
        preview_url = str(item.get('preview_url') or '').strip()
        if not preview_url:
            continue
        if not fallback_preview:
            fallback_preview = preview_url

        item_language = str(item.get('language') or '').strip().lower()
        item_accent = str(item.get('accent') or '').strip().lower()
        language_matches = not normalized_language or item_language == normalized_language
        accent_matches = not normalized_accent or item_accent == normalized_accent
        if language_matches and accent_matches:
            return preview_url

    return fallback_preview


def _serialize_shared_voice(voice, *, language='', accent=''):
    safe_language = str(voice.get('language') or '').strip().lower()
    safe_accent = str(voice.get('accent') or '').strip().lower()
    preview_url = (
        str(voice.get('preview_url') or '').strip()
        or _first_verified_language_preview(voice, language=language, accent=accent)
    )

    return {
        'voice_id': voice.get('voice_id') or '',
        'name': voice.get('name') or '',
        'category': voice.get('category') or '',
        'api_usable': True,
        'requires_subscription': False,
        'matches_filter': True,
        'preview_url': preview_url,
        'description': voice.get('description') or '',
        'public_owner_id': voice.get('public_owner_id') or '',
        'is_library': True,
        'is_added_by_user': bool(voice.get('is_added_by_user')),
        'is_bookmarked': bool(voice.get('is_bookmarked')),
        'free_users_allowed': bool(voice.get('free_users_allowed')),
        'cloned_by_count': _safe_int(voice.get('cloned_by_count'), 0),
        'labels': {
            'language': safe_language,
            'accent': safe_accent,
            'gender': voice.get('gender') or '',
            'age': voice.get('age') or '',
            'descriptive': voice.get('descriptive') or '',
            'use_case': voice.get('use_case') or '',
        },
    }


def _custom_voice_item(
    voice_id,
    name='',
    *,
    matches_filter=False,
    labels=None,
    category='custom',
    is_custom=True,
    sort_priority=100,
    preview_url='',
):
    safe_name = str(name or '').strip()
    safe_labels = labels or {}
    return {
        'voice_id': voice_id,
        'name': safe_name or f'Voix personnalisee ({voice_id})',
        'category': category,
        'api_usable': True,
        'requires_subscription': False,
        'matches_filter': bool(matches_filter),
        'is_custom': bool(is_custom),
        'sort_priority': int(sort_priority),
        'preview_url': str(preview_url or '').strip(),
        'labels': {
            'language': safe_labels.get('language') or '',
            'accent': safe_labels.get('accent') or '',
            'gender': safe_labels.get('gender') or '',
            'age': safe_labels.get('age') or '',
            'descriptive': safe_labels.get('descriptive') or '',
            'use_case': safe_labels.get('use_case') or '',
        },
    }


def _extra_voice_items():
    items = [
        _custom_voice_item(
            item['voice_id'],
            name=item.get('name', ''),
            matches_filter=True,
            labels=item.get('labels') or {},
            category=item.get('category', ''),
            is_custom=item.get('is_custom', False),
            sort_priority=item.get('sort_priority', 100),
            preview_url=item.get('preview_url', ''),
        )
        for item in BUILTIN_EXTRA_VOICES
    ]

    raw = str(getattr(settings, 'ELEVENLABS_EXTRA_VOICES', '') or '').strip()
    if not raw:
        return items

    for entry in raw.split(','):
        clean_entry = entry.strip()
        if not clean_entry:
            continue

        if ':' in clean_entry:
            name, voice_id = clean_entry.split(':', 1)
        else:
            name, voice_id = '', clean_entry

        voice_id = voice_id.strip()
        if not voice_id:
            continue
        items.append(_custom_voice_item(voice_id, name=name, matches_filter=True))

    return items


def _apply_voice_override(existing, override):
    labels = existing.get('labels') or {}
    override_labels = override.get('labels') or {}
    existing.update({
        'name': override.get('name') or existing.get('name') or '',
        'category': override.get('category', existing.get('category', '')),
        'api_usable': override.get('api_usable', existing.get('api_usable', True)),
        'requires_subscription': override.get(
            'requires_subscription',
            existing.get('requires_subscription', False),
        ),
        'matches_filter': bool(existing.get('matches_filter') or override.get('matches_filter')),
        'is_custom': override.get('is_custom', existing.get('is_custom', False)),
        'sort_priority': override.get('sort_priority', existing.get('sort_priority', 100)),
        'preview_url': override.get('preview_url') or existing.get('preview_url', ''),
        'labels': {
            **labels,
            **{key: value for key, value in override_labels.items() if value},
        },
    })


def list_shared_voices(
    *,
    language='fr',
    accent='parisian',
    category='',
    gender='',
    age='',
    search='',
    featured=False,
    page_size=60,
    page=0,
):
    api_key = getattr(settings, 'ELEVENLABS_API_KEY', '').strip()
    if not api_key:
        raise ElevenLabsConfigurationError('ELEVENLABS_API_KEY non configure.')

    safe_page_size = max(1, min(_safe_int(page_size, 60), 100))
    safe_page = max(0, _safe_int(page, 0))
    allowed_categories = {'professional', 'famous', 'high_quality'}
    allowed_genders = {'male', 'female', 'neutral'}
    allowed_ages = {'young', 'middle_aged', 'old'}
    normalized_category = str(category or '').strip().lower()
    normalized_gender = str(gender or '').strip().lower()
    normalized_age = str(age or '').strip().lower().replace('-', '_').replace(' ', '_')
    safe_featured = _safe_bool(featured, False)

    params = {
        'page_size': safe_page_size,
        'page': safe_page,
    }
    for key, value in (
        ('language', language),
        ('accent', accent),
        ('search', search),
    ):
        safe_value = str(value or '').strip()
        if safe_value:
            params[key] = safe_value

    if normalized_category in allowed_categories:
        params['category'] = normalized_category
    if normalized_gender in allowed_genders:
        params['gender'] = normalized_gender
    if normalized_age in allowed_ages:
        params['age'] = normalized_age
    if safe_featured:
        params['featured'] = True

    try:
        response = requests.get(
            'https://api.elevenlabs.io/v1/shared-voices',
            headers={'xi-api-key': api_key},
            params=params,
            timeout=float(getattr(settings, 'ELEVENLABS_TIMEOUT_SECONDS', 60) or 60),
        )
    except requests.Timeout as exc:
        raise ElevenLabsAPIError('Timeout ElevenLabs pendant le chargement de la Voice Library.') from exc
    except requests.RequestException as exc:
        raise ElevenLabsAPIError('Erreur reseau ElevenLabs pendant le chargement de la Voice Library.') from exc

    if response.status_code >= 400:
        detail = _extract_error_detail(response)
        raise ElevenLabsAPIError(f'ElevenLabs HTTP {response.status_code}: {detail}')

    try:
        payload = response.json()
    except ValueError as exc:
        raise ElevenLabsAPIError('ElevenLabs a retourne une Voice Library invalide.') from exc

    if not isinstance(payload, dict):
        payload = {}
    voices = payload.get('voices', [])
    if not isinstance(voices, list):
        voices = []

    normalized_language = str(language or '').strip().lower()
    normalized_accent = str(accent or '').strip().lower()
    serialized = [
        _serialize_shared_voice(voice, language=normalized_language, accent=normalized_accent)
        for voice in voices
        if isinstance(voice, dict) and voice.get('voice_id')
    ]

    return {
        'voices': serialized,
        'has_more': bool(payload.get('has_more')),
        'total_count': _safe_int(payload.get('total_count'), len(serialized)),
        'last_sort_id': payload.get('last_sort_id') or '',
        'filters': {
            'language': normalized_language,
            'accent': normalized_accent,
            'category': normalized_category if normalized_category in allowed_categories else '',
            'gender': normalized_gender if normalized_gender in allowed_genders else '',
            'age': normalized_age if normalized_age in allowed_ages else '',
            'search': str(search or '').strip(),
            'featured': safe_featured,
            'page_size': safe_page_size,
            'page': safe_page,
        },
    }


def list_filtered_voices(*, language='fr', accent='parisian', include_fallback=True):
    api_key = getattr(settings, 'ELEVENLABS_API_KEY', '').strip()
    if not api_key:
        raise ElevenLabsConfigurationError('ELEVENLABS_API_KEY non configure.')

    try:
        response = requests.get(
            'https://api.elevenlabs.io/v1/voices',
            headers={'xi-api-key': api_key},
            timeout=float(getattr(settings, 'ELEVENLABS_TIMEOUT_SECONDS', 60) or 60),
        )
    except requests.Timeout as exc:
        raise ElevenLabsAPIError('Timeout ElevenLabs pendant le chargement des voix.') from exc
    except requests.RequestException as exc:
        raise ElevenLabsAPIError('Erreur reseau ElevenLabs pendant le chargement des voix.') from exc

    if response.status_code >= 400:
        detail = _extract_error_detail(response)
        raise ElevenLabsAPIError(f'ElevenLabs HTTP {response.status_code}: {detail}')

    try:
        voices = response.json().get('voices', [])
    except ValueError as exc:
        raise ElevenLabsAPIError('ElevenLabs a retourne une liste de voix invalide.') from exc

    normalized_language = str(language or '').strip().lower()
    normalized_accent = str(accent or '').strip().lower()
    filtered = []
    seen_voice_ids = set()

    for voice in voices:
        labels = voice.get('labels') or {}
        voice_language = str(labels.get('language') or '').strip().lower()
        voice_accent = str(labels.get('accent') or '').strip().lower()
        if normalized_language and voice_language != normalized_language:
            continue
        if normalized_accent and voice_accent != normalized_accent:
            continue

        serialized = _serialize_voice(voice, matches_filter=True)
        filtered.append(serialized)
        seen_voice_ids.add(serialized['voice_id'])

    has_usable_filtered_voice = any(voice.get('api_usable') for voice in filtered)
    if include_fallback and not has_usable_filtered_voice:
        for voice in voices:
            if voice.get('category') != 'premade':
                continue
            if voice.get('voice_id') in seen_voice_ids:
                continue
            serialized = _serialize_voice(voice, matches_filter=False)
            filtered.append(serialized)
            seen_voice_ids.add(serialized['voice_id'])

    default_voice_id = getattr(settings, 'ELEVENLABS_VOICE_ID', '').strip()
    if default_voice_id and default_voice_id not in seen_voice_ids:
        filtered.insert(0, _custom_voice_item(default_voice_id))
        seen_voice_ids.add(default_voice_id)

    for voice in _extra_voice_items():
        voice_id = voice.get('voice_id')
        if not voice_id:
            continue
        if voice_id in seen_voice_ids:
            existing = next((item for item in filtered if item.get('voice_id') == voice_id), None)
            if existing:
                _apply_voice_override(existing, voice)
            continue
        filtered.append(voice)
        seen_voice_ids.add(voice_id)

    return sorted(
        filtered,
        key=lambda item: (
            item.get('sort_priority', 100),
            not item.get('is_custom'),
            not item.get('matches_filter'),
            not item.get('api_usable'),
            (item.get('name') or '').lower(),
        ),
    )
