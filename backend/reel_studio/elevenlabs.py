import logging
import re

import requests
from django.conf import settings


logger = logging.getLogger(__name__)


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


def generate_speech_mp3(
    *,
    text,
    voice_id='',
    model_id='',
    output_format='',
):
    api_key = getattr(settings, 'ELEVENLABS_API_KEY', '').strip()
    resolved_voice_id = (voice_id or getattr(settings, 'ELEVENLABS_VOICE_ID', '')).strip()
    resolved_model_id = (model_id or getattr(settings, 'ELEVENLABS_MODEL_ID', '')).strip()
    resolved_output_format = (
        output_format or getattr(settings, 'ELEVENLABS_OUTPUT_FORMAT', 'mp3_44100_128')
    ).strip()
    language_code = getattr(settings, 'ELEVENLABS_LANGUAGE_CODE', '').strip()
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
            'stability': float(getattr(settings, 'ELEVENLABS_VOICE_STABILITY', 0.45)),
            'similarity_boost': float(getattr(settings, 'ELEVENLABS_VOICE_SIMILARITY_BOOST', 0.8)),
            'style': float(getattr(settings, 'ELEVENLABS_VOICE_STYLE', 0.0)),
            'use_speaker_boost': bool(getattr(settings, 'ELEVENLABS_USE_SPEAKER_BOOST', True)),
        },
    }
    if language_code:
        payload['language_code'] = language_code

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
