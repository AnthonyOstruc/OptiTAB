import base64
import re
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import requests
from django.conf import settings


SITE_REFERENCE_DIR = Path(__file__).resolve().parent / 'site_references'
SITE_REFERENCE_MAX_BYTES = 4 * 1024 * 1024
SITE_REFERENCE_MAX_COUNT = 6
SITE_REFERENCE_MIME_BY_SUFFIX = {
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.webp': 'image/webp',
}

IMAGE_INSTRUCTIONS_FILE = Path(__file__).resolve().parent / 'image_instructions.txt'
IMAGE_INSTRUCTIONS_MAX_LENGTH = 6000


def read_image_instructions():
    try:
        text = IMAGE_INSTRUCTIONS_FILE.read_text(encoding='utf-8')
    except OSError:
        return ''
    return text.strip()


def write_image_instructions(text):
    cleaned = str(text or '').replace('\r\n', '\n').strip()
    if len(cleaned) > IMAGE_INSTRUCTIONS_MAX_LENGTH:
        cleaned = cleaned[:IMAGE_INSTRUCTIONS_MAX_LENGTH]
    IMAGE_INSTRUCTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    IMAGE_INSTRUCTIONS_FILE.write_text(cleaned, encoding='utf-8')
    return cleaned


class GeminiConfigurationError(Exception):
    pass


class GeminiAPIError(Exception):
    pass


PRICING_SOURCE = 'https://ai.google.dev/gemini-api/docs/pricing'
USD_PRECISION = Decimal('0.00000001')

GEMINI_PRICING_STANDARD = {
    # Image generation models (Nano Banana family)
    'gemini-2.5-flash-image': {'input': Decimal('0.30'), 'output': Decimal('30.00')},
    'gemini-3.1-flash-image-preview': {'input': Decimal('0.30'), 'output': Decimal('30.00')},
    'gemini-3-pro-image-preview': {'input': Decimal('1.25'), 'output': Decimal('60.00')},
    # Text / multimodal models
    'gemini-2.5-pro': {'input': Decimal('1.25'), 'output': Decimal('10.00')},
    'gemini-2.5-flash': {'input': Decimal('0.30'), 'output': Decimal('2.50')},
    'gemini-2.5-flash-lite': {'input': Decimal('0.10'), 'output': Decimal('0.40')},
    'gemini-2.0-flash': {'input': Decimal('0.10'), 'output': Decimal('0.40')},
    'gemini-2.0-flash-lite': {'input': Decimal('0.075'), 'output': Decimal('0.30')},
    'gemini-1.5-pro': {'input': Decimal('1.25'), 'output': Decimal('5.00')},
    'gemini-1.5-flash': {'input': Decimal('0.075'), 'output': Decimal('0.30')},
}

FALLBACK_GEMINI_MODELS = [
    {'id': 'gemini-2.5-flash', 'display_name': 'Gemini 2.5 Flash'},
    {'id': 'gemini-2.5-pro', 'display_name': 'Gemini 2.5 Pro'},
    {'id': 'gemini-2.5-flash-lite', 'display_name': 'Gemini 2.5 Flash-Lite'},
    {'id': 'gemini-2.0-flash', 'display_name': 'Gemini 2.0 Flash'},
]

# Real native image generation models (Nano Banana family)
FALLBACK_GEMINI_IMAGE_MODELS = [
    {'id': 'gemini-2.5-flash-image', 'display_name': 'Nano Banana (Gemini 2.5 Flash Image)'},
    {'id': 'gemini-3.1-flash-image-preview', 'display_name': 'Nano Banana 2 (Gemini 3.1 Flash Image preview)'},
    {'id': 'gemini-3-pro-image-preview', 'display_name': 'Nano Banana Pro (Gemini 3 Pro Image preview)'},
]


def _clean_model_id(model_id):
    value = str(model_id or '').strip() or getattr(settings, 'GEMINI_MODEL_ID', 'gemini-2.5-flash')
    if value.startswith('models/'):
        value = value.split('/', 1)[1]
    if not re.match(r'^[A-Za-z0-9_.-]+$', value):
        raise GeminiConfigurationError('Modele Gemini invalide.')
    return value


def _strip_markdown_fences(value):
    text = str(value or '').strip()
    match = re.match(r'^```(?:[A-Za-z0-9_-]+)?\s*(.*?)\s*```$', text, flags=re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def _extract_text_payload(data):
    chunks = []
    for candidate in data.get('candidates') or []:
        content = candidate.get('content') or {}
        for part in content.get('parts') or []:
            text = part.get('text')
            if text:
                chunks.append(str(text))

    text_payload = '\n'.join(chunks).strip()
    if not text_payload:
        raise GeminiAPIError('Gemini n a renvoye aucun texte exploitable.')
    return _strip_markdown_fences(text_payload)


def _extract_image_payload(data):
    text_chunks = []
    for candidate in data.get('candidates') or []:
        content = candidate.get('content') or {}
        for part in content.get('parts') or []:
            text = part.get('text')
            if text:
                text_chunks.append(str(text))
            inline_data = part.get('inlineData') or part.get('inline_data') or {}
            if not isinstance(inline_data, dict):
                continue
            raw_data = inline_data.get('data')
            if not raw_data:
                continue
            mime_type = inline_data.get('mimeType') or inline_data.get('mime_type') or 'image/png'
            try:
                image_bytes = base64.b64decode(str(raw_data), validate=True)
            except (ValueError, TypeError) as exc:
                raise GeminiAPIError('Gemini a renvoye une image invalide.') from exc
            if image_bytes:
                return {
                    'image_bytes': image_bytes,
                    'mime_type': mime_type,
                    'text': '\n'.join(text_chunks).strip(),
                }

    detail = '\n'.join(text_chunks).strip()
    if detail:
        raise GeminiAPIError(f'Gemini a renvoye du texte au lieu d une image: {detail[:300]}')
    raise GeminiAPIError('Gemini n a renvoye aucune image exploitable.')


def _load_site_reference_parts():
    if not SITE_REFERENCE_DIR.exists():
        return []
    parts = []
    try:
        entries = sorted(SITE_REFERENCE_DIR.iterdir(), key=lambda p: p.name.lower())
    except OSError:
        return []
    for path in entries:
        if len(parts) >= SITE_REFERENCE_MAX_COUNT:
            break
        if not path.is_file():
            continue
        mime = SITE_REFERENCE_MIME_BY_SUFFIX.get(path.suffix.lower())
        if not mime:
            continue
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if size <= 0 or size > SITE_REFERENCE_MAX_BYTES:
            continue
        try:
            with open(path, 'rb') as fh:
                raw = fh.read()
        except OSError:
            continue
        parts.append({
            'inlineData': {
                'mimeType': mime,
                'data': base64.b64encode(raw).decode('ascii'),
            }
        })
    return parts


def _error_detail(response):
    try:
        data = response.json()
    except ValueError:
        return response.text[:500] if response.text else response.reason

    error = data.get('error') if isinstance(data, dict) else None
    if isinstance(error, dict):
        return error.get('message') or str(error)
    return str(data)[:500]


def _model_pricing(model_id):
    return GEMINI_PRICING_STANDARD.get(_clean_model_id(model_id))


def _decimal_cost(token_count, price_per_million):
    tokens = Decimal(str(int(token_count or 0)))
    return ((tokens / Decimal('1000000')) * price_per_million).quantize(
        USD_PRECISION,
        rounding=ROUND_HALF_UP,
    )


def extract_usage_metadata(data):
    metadata = data.get('usageMetadata') if isinstance(data, dict) else {}
    if not isinstance(metadata, dict):
        metadata = {}

    prompt_tokens = int(metadata.get('promptTokenCount') or 0)
    candidates_tokens = int(metadata.get('candidatesTokenCount') or 0)
    thoughts_tokens = int(metadata.get('thoughtsTokenCount') or 0)
    total_tokens = int(metadata.get('totalTokenCount') or 0)
    output_tokens = candidates_tokens + thoughts_tokens
    if total_tokens and prompt_tokens and output_tokens <= 0:
        output_tokens = max(total_tokens - prompt_tokens, 0)

    return {
        'prompt_token_count': prompt_tokens,
        'candidates_token_count': candidates_tokens,
        'thoughts_token_count': thoughts_tokens,
        'total_token_count': total_tokens,
        'billable_output_token_count': output_tokens,
    }


def estimate_gemini_cost(*, model_id, usage):
    pricing = _model_pricing(model_id)
    if not pricing:
        zero = Decimal('0').quantize(USD_PRECISION)
        return {
            'input_cost_usd': zero,
            'output_cost_usd': zero,
            'total_cost_usd': zero,
            'pricing_known': False,
            'pricing_source': '',
        }

    input_cost = _decimal_cost(usage.get('prompt_token_count', 0), pricing['input'])
    output_cost = _decimal_cost(usage.get('billable_output_token_count', 0), pricing['output'])
    return {
        'input_cost_usd': input_cost,
        'output_cost_usd': output_cost,
        'total_cost_usd': (input_cost + output_cost).quantize(USD_PRECISION),
        'pricing_known': True,
        'pricing_source': PRICING_SOURCE,
    }


def _model_payload(model_id, display_name=''):
    clean_id = _clean_model_id(model_id)
    pricing = _model_pricing(clean_id)
    return {
        'id': clean_id,
        'display_name': display_name or clean_id,
        'input_price_per_1m_tokens': str(pricing['input']) if pricing else '',
        'output_price_per_1m_tokens': str(pricing['output']) if pricing else '',
        'pricing_known': bool(pricing),
        'pricing_source': PRICING_SOURCE if pricing else '',
    }


def fallback_models_payload():
    return [_model_payload(item['id'], item['display_name']) for item in FALLBACK_GEMINI_MODELS]


def list_gemini_models():
    api_key = str(getattr(settings, 'GEMINI_API_KEY', '') or '').strip()
    if not api_key:
        return fallback_models_payload()

    api_url = str(
        getattr(settings, 'GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta')
    ).rstrip('/')
    url = f'{api_url}/models'

    try:
        response = requests.get(
            url,
            headers={'x-goog-api-key': api_key},
            timeout=getattr(settings, 'GEMINI_TIMEOUT_SECONDS', 60.0),
        )
    except requests.RequestException:
        return fallback_models_payload()

    if response.status_code >= 400:
        return fallback_models_payload()

    try:
        data = response.json()
    except ValueError:
        return fallback_models_payload()

    models = []
    for item in data.get('models') or []:
        methods = item.get('supportedGenerationMethods') or []
        if 'generateContent' not in methods:
            continue
        raw_name = str(item.get('name') or '').strip()
        if not raw_name:
            continue
        model_id = raw_name.split('/', 1)[1] if raw_name.startswith('models/') else raw_name
        try:
            models.append(_model_payload(model_id, item.get('displayName') or model_id))
        except GeminiConfigurationError:
            continue

    fallback_by_id = {item['id']: item for item in fallback_models_payload()}
    merged = {item['id']: item for item in models}
    merged.update({model_id: model for model_id, model in fallback_by_id.items() if model_id not in merged})

    return sorted(
        merged.values(),
        key=lambda model: (
            0 if model['id'] == getattr(settings, 'GEMINI_MODEL_ID', 'gemini-2.5-flash') else 1,
            model['id'],
        ),
    )


def generate_carousel_template(*, prompt, model_id='', return_metadata=False):
    api_key = str(getattr(settings, 'GEMINI_API_KEY', '') or '').strip()
    if not api_key:
        raise GeminiConfigurationError('GEMINI_API_KEY manquant cote backend.')

    safe_prompt = str(prompt or '').strip()
    if not safe_prompt:
        raise GeminiConfigurationError('Prompt Gemini vide.')

    model = _clean_model_id(model_id)
    api_url = str(
        getattr(settings, 'GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta')
    ).rstrip('/')
    url = f'{api_url}/models/{model}:generateContent'

    payload = {
        'contents': [
            {
                'role': 'user',
                'parts': [{'text': safe_prompt}],
            }
        ],
        'generationConfig': {
            'temperature': getattr(settings, 'GEMINI_TEMPERATURE', 0.65),
            'maxOutputTokens': getattr(settings, 'GEMINI_MAX_OUTPUT_TOKENS', 8192),
        },
    }

    try:
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'x-goog-api-key': api_key,
            },
            json=payload,
            timeout=getattr(settings, 'GEMINI_TIMEOUT_SECONDS', 60.0),
        )
    except requests.RequestException as exc:
        raise GeminiAPIError(f'Erreur reseau Gemini: {exc}') from exc

    if response.status_code >= 400:
        raise GeminiAPIError(f'Erreur Gemini {response.status_code}: {_error_detail(response)}')

    try:
        data = response.json()
    except ValueError as exc:
        raise GeminiAPIError('Reponse Gemini invalide.') from exc

    text = _extract_text_payload(data)
    usage = extract_usage_metadata(data)
    cost = estimate_gemini_cost(model_id=model, usage=usage)
    if return_metadata:
        return {
            'text': text,
            'model_id': model,
            'usage': usage,
            'cost': cost,
        }
    return text


_GEMINI_SUPPORTED_ASPECT_RATIOS = {'1:1', '3:4', '4:3', '9:16', '16:9'}


def generate_carousel_image(*, prompt, model_id='', aspect_ratio='4:5', return_metadata=False, use_site_references=True):
    api_key = str(getattr(settings, 'GEMINI_API_KEY', '') or '').strip()
    if not api_key:
        raise GeminiConfigurationError('GEMINI_API_KEY manquant cote backend.')

    safe_prompt = str(prompt or '').strip()
    if not safe_prompt:
        raise GeminiConfigurationError('Prompt image Gemini vide.')

    model = _clean_model_id(model_id or getattr(settings, 'GEMINI_IMAGE_MODEL_ID', 'gemini-2.5-flash-image'))
    api_url = str(
        getattr(settings, 'GEMINI_API_URL', 'https://generativelanguage.googleapis.com/v1beta')
    ).rstrip('/')
    url = f'{api_url}/models/{model}:generateContent'

    requested_ratio = str(aspect_ratio or '').strip()
    api_ratio = requested_ratio if requested_ratio in _GEMINI_SUPPORTED_ASPECT_RATIOS else '3:4'

    user_instructions = read_image_instructions()
    reference_parts = _load_site_reference_parts() if use_site_references else []
    if reference_parts:
        prompt_text = (
            "REFERENCE IMAGES: the attached images are real screenshots of the "
            "OptiTAB interface (optitab.net). They define EXACTLY how the product "
            "looks: palette (OptiTAB blue #29428e, white, soft pastel accents), "
            "blue header bar, left sidebar navigation, dashboard with leaderboard "
            "and XP cards, chapter / lesson cards layout, button styles, OptiTAB "
            "logo, typography.\n\n"
            "IMPORTANT: when the scene you generate contains any device screen "
            "(laptop, smartphone, tablet), REPRODUCE the OptiTAB interface shown "
            "in the references as faithfully as possible inside that screen. "
            "Match the cards, colors, sidebar, header, layout, logo placement, "
            "and overall feel. Use the references as the single source of truth "
            "for what OptiTAB looks like.\n\n"
            "The environment AROUND the device (desk, light, background) is "
            "what you compose freely, while keeping clean space for a text "
            "overlay added later.\n\n"
            + safe_prompt
        )
    else:
        prompt_text = safe_prompt

    if user_instructions:
        prompt_text = (
            "PERMANENT USER INSTRUCTIONS (apply to every image you generate, "
            "they override any conflicting default direction below):\n"
            f"{user_instructions}\n\n---\n\n"
            + prompt_text
        )

    payload = {
        'contents': [
            {
                'role': 'user',
                'parts': [
                    *reference_parts,
                    {'text': prompt_text},
                ],
            }
        ],
        'generationConfig': {
            'responseModalities': ['IMAGE'],
        },
    }

    try:
        response = requests.post(
            url,
            headers={
                'Content-Type': 'application/json',
                'x-goog-api-key': api_key,
            },
            json=payload,
            timeout=getattr(settings, 'GEMINI_IMAGE_TIMEOUT_SECONDS', 180.0),
        )
    except requests.RequestException as exc:
        raise GeminiAPIError(f'Erreur reseau Gemini image: {exc}') from exc

    if response.status_code >= 400:
        raise GeminiAPIError(f'Erreur Gemini image {response.status_code}: {_error_detail(response)}')

    try:
        data = response.json()
    except ValueError as exc:
        raise GeminiAPIError('Reponse Gemini image invalide.') from exc

    image_payload = _extract_image_payload(data)
    usage = extract_usage_metadata(data)
    cost = estimate_gemini_cost(model_id=model, usage=usage)
    if return_metadata:
        return {
            **image_payload,
            'model_id': model,
            'usage': usage,
            'cost': cost,
        }
    return image_payload['image_bytes']
