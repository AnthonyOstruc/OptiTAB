import logging
import re

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.http import FileResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.text import slugify
from rest_framework.negotiation import BaseContentNegotiation
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ReelProject, ReelSlide
from .permissions import IsStaffOrSuperuser
from .serializers import (
    ReelProjectDetailSerializer,
    ReelProjectSerializer,
    ReelSlideSerializer,
    ReelSpeechGenerateSerializer,
    ReelTTSTestSerializer,
    ReelTemplateGenerateSerializer,
    ReelVideoExportSerializer,
)
from .elevenlabs import (
    ElevenLabsAPIError,
    ElevenLabsConfigurationError,
    build_slide_speech_text,
    build_project_speech_text,
    generate_speech_mp3,
    list_filtered_voices,
)
from .tts import (
    PROVIDER_ELEVENLABS,
    PROVIDER_GOOGLE,
    SUPPORTED_PROVIDERS,
    TTSAPIError,
    TTSConfigurationError,
    TTSQuotaExceeded,
    generate_speech as tts_generate_speech,
    list_providers_payload,
)


tts_logger = logging.getLogger('reel_studio.tts')
from .video_export import (
    VideoExportConfigurationError,
    VideoExportError,
    export_reel_video,
)


DEMO_SLIDES = [
    {
        'slide_type': ReelSlide.TYPE_HOOK,
        'title': '',
        'screen_text': '99 % se trompent ici',
        'katex': '',
        'voice_script': "Attention, cette dérivée piège beaucoup d’élèves.",
        'duration_seconds': 4,
    },
    {
        'slide_type': ReelSlide.TYPE_KATEX,
        'title': 'Dérivée piégeuse',
        'screen_text': '',
        'katex': '\\begin{aligned}\n&f(x)=x\\ln(x)\n\\end{aligned}',
        'voice_script': 'On veut dériver x fois ln de x.',
        'duration_seconds': 5,
    },
    {
        'slide_type': ReelSlide.TYPE_CUMULATIVE_KATEX,
        'title': 'On reconnaît un produit',
        'screen_text': '',
        'katex': '\\begin{aligned}\n&f(x)=x\\ln(x)\\\\[0.4em]\n&u=x \\qquad v=\\ln(x)\n\\end{aligned}',
        'voice_script': 'Ici, on reconnaît un produit.',
        'duration_seconds': 5,
    },
    {
        'slide_type': ReelSlide.TYPE_CUMULATIVE_KATEX,
        'title': 'On dérive',
        'screen_text': '',
        'katex': "\\begin{aligned}\n&u=x \\qquad v=\\ln(x)\\\\[0.4em]\n&u'=1 \\qquad v'=\\frac{1}{x}\n\\end{aligned}",
        'voice_script': 'On dérive chaque facteur séparément.',
        'duration_seconds': 5,
    },
    {
        'slide_type': ReelSlide.TYPE_RESULT,
        'title': 'Résultat',
        'screen_text': '',
        'katex': "\\begin{aligned}\n&f'(x)=u'v+uv'\\\\[0.4em]\n&f'(x)=\\ln(x)+x\\cdot\\frac{1}{x}\\\\[0.4em]\n&f'(x)=\\ln(x)+1\n\\end{aligned}",
        'voice_script': 'Donc la dérivée est ln de x plus un.',
        'duration_seconds': 6,
    },
    {
        'slide_type': ReelSlide.TYPE_CTA,
        'title': 'Résultat',
        'screen_text': 'Abonne-toi à OptiTAB\nSauvegarde ce Reel\nCommente ton résultat',
        'katex': "f'(x)=\\ln(x)+1",
        'voice_script': 'Abonne-toi à OptiTAB pour progresser en maths.',
        'duration_seconds': 4,
    },
]


class ReelDownloadContentNegotiation(BaseContentNegotiation):
    def select_parser(self, request, parsers):
        return parsers[0] if parsers else None

    def select_renderer(self, request, renderers, format_suffix=None):
        renderer = renderers[0]
        return renderer, renderer.media_type
DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS = 4
DEFAULT_CTA_TEXT = 'Abonne-toi à OptiTAB\nSauvegarde ce Reel\nCommente ton résultat'
LEGACY_CTA_TEXTS = {
    "Abonne-toi à OptiTAB pour d'autres défis maths",
    "Abonne-toi à OptiTAB\npour d'autres défis maths",
    'Abonne-toi à OptiTAB | Sauvegarde ce Reel et commente ton résultat',
    'Abonne-toi à OptiTAB\nSauvegarde ce Reel et commente ton résultat',
    'Abonne-toi pour éviter les pièges',
}


def _touch_project(project_id):
    ReelProject.objects.filter(pk=project_id).update(updated_at=timezone.now())


def _project_serializer(project, request, *, detail=False):
    serializer_cls = ReelProjectDetailSerializer if detail else ReelProjectSerializer
    return serializer_cls(project, context={'request': request})


def _project_video_download_filename(project):
    safe_title = slugify(project.title or '') or f'reel-{project.pk}'
    return f'{safe_title}.mp4'


def _slide_serializer(slide, request):
    return ReelSlideSerializer(slide, context={'request': request})


def _clear_slide_speech(slide):
    previous_audio_name = slide.speech_audio.name if slide.speech_audio else ''
    slide.speech_audio = None
    slide.speech_text = ''
    slide.speech_voice_id = ''
    slide.speech_model_id = ''
    slide.speech_output_format = ''
    slide.speech_status = ReelProject.SPEECH_STATUS_EMPTY
    slide.speech_error = ''
    slide.speech_generated_at = None
    slide.save(
        update_fields=[
            'speech_audio',
            'speech_text',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'updated_at',
        ]
    )
    if previous_audio_name:
        try:
            default_storage.delete(previous_audio_name)
        except Exception:
            pass


def _clear_project_speech(project):
    previous_audio_name = project.speech_audio.name if project.speech_audio else ''
    project.speech_audio = None
    project.speech_text = ''
    project.speech_voice_id = ''
    project.speech_model_id = ''
    project.speech_output_format = ''
    project.speech_status = ReelProject.SPEECH_STATUS_EMPTY
    project.speech_error = ''
    project.speech_generated_at = None
    project.save(
        update_fields=[
            'speech_audio',
            'speech_text',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'updated_at',
        ]
    )
    if previous_audio_name:
        try:
            default_storage.delete(previous_audio_name)
        except Exception:
            pass


def _clear_project_video(project):
    previous_video_name = project.video_file.name if project.video_file else ''
    project.video_file = None
    project.video_status = ReelProject.VIDEO_STATUS_EMPTY
    project.video_error = ''
    project.video_generated_at = None
    project.save(
        update_fields=[
            'video_file',
            'video_status',
            'video_error',
            'video_generated_at',
            'updated_at',
        ]
    )
    if previous_video_name:
        try:
            default_storage.delete(previous_video_name)
        except Exception:
            pass


def _speech_compare_text(value):
    return re.sub(r'\s+', ' ', str(value or '')).strip()


def _common_slide_speech_value(slides, field_name):
    values = {
        str(getattr(slide, field_name, '') or '').strip()
        for slide in slides
        if str(getattr(slide, field_name, '') or '').strip()
    }
    if len(values) == 1:
        return next(iter(values))
    if len(values) > 1:
        return 'mixed'
    return ''


def _sync_project_speech_from_slides(project_or_id):
    if isinstance(project_or_id, ReelProject):
        project = project_or_id
    else:
        project = ReelProject.objects.get(pk=project_or_id)

    slides = list(project.slides.all().order_by('order', 'id'))
    expected_entries = [
        (slide, build_slide_speech_text(slide))
        for slide in slides
    ]
    expected_entries = [
        (slide, speech_text)
        for slide, speech_text in expected_entries
        if speech_text
    ]

    if not expected_entries:
        _clear_project_speech(project)
        return project

    previous_audio_name = project.speech_audio.name if project.speech_audio else ''
    ready_slides = []
    error_slides = []

    for slide, expected_text in expected_entries:
        if slide.speech_status == ReelProject.SPEECH_STATUS_ERROR:
            error_slides.append(slide)

        if (
            slide.speech_audio
            and slide.speech_status == ReelProject.SPEECH_STATUS_READY
            and _speech_compare_text(slide.speech_text) == _speech_compare_text(expected_text)
        ):
            ready_slides.append(slide)

    project.speech_audio = None
    project.speech_text = '\n\n'.join(speech_text for _, speech_text in expected_entries)
    project.speech_voice_id = _common_slide_speech_value(ready_slides, 'speech_voice_id')
    project.speech_model_id = _common_slide_speech_value(ready_slides, 'speech_model_id')
    project.speech_output_format = _common_slide_speech_value(ready_slides, 'speech_output_format')

    if len(ready_slides) == len(expected_entries):
        project.speech_status = ReelProject.SPEECH_STATUS_READY
        project.speech_error = ''
    elif error_slides:
        project.speech_status = ReelProject.SPEECH_STATUS_ERROR
        project.speech_error = 'Un ou plusieurs MP3 de slide sont en erreur.'
    else:
        project.speech_status = ReelProject.SPEECH_STATUS_EMPTY
        project.speech_error = ''

    generated_dates = [
        slide.speech_generated_at
        for slide in ready_slides
        if slide.speech_generated_at
    ]
    project.speech_generated_at = max(generated_dates) if generated_dates else None
    project.save(
        update_fields=[
            'speech_audio',
            'speech_text',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'updated_at',
        ]
    )

    if previous_audio_name:
        try:
            default_storage.delete(previous_audio_name)
        except Exception:
            pass

    return project


def _collect_video_export_audio_issues(project, frames):
    slides_by_id = {slide.pk: slide for slide in project.slides.all()}
    issues = []

    for frame in frames:
        slide_id = int(frame.get('slide_id') or 0)
        slide = slides_by_id.get(slide_id)
        if not slide:
            continue

        expected_speech = _speech_compare_text(build_slide_speech_text(slide))
        if not expected_speech:
            continue

        slide_label = f'Slide {slide.order}'
        if not slide.speech_audio:
            issues.append(f'{slide_label}: MP3 voix manquant.')
            continue

        if slide.speech_status != ReelProject.SPEECH_STATUS_READY:
            issues.append(f'{slide_label}: MP3 voix pas pret.')
            continue

        if _speech_compare_text(slide.speech_text) != expected_speech:
            issues.append(f'{slide_label}: MP3 voix pas a jour, regenere la voix.')

    return issues


def _generate_and_save_slide_speech(
    slide,
    *,
    speech_text,
    provider='',
    voice_id='',
    model_id='',
    output_format='',
):
    safe_speech_text = str(speech_text or '').strip()
    if not safe_speech_text:
        raise ValueError('Aucun texte voix disponible pour cette slide.')

    slide.speech_status = ReelProject.SPEECH_STATUS_EMPTY
    slide.speech_error = ''
    slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])

    result = tts_generate_speech(
        text=safe_speech_text,
        provider=provider,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
    )

    tts_logger.info(
        'Slide speech generated | slide_id=%s | provider=%s | voice=%s | chars=%d | cached=%s',
        slide.pk,
        result.provider,
        result.voice_id,
        result.character_count,
        result.cached,
    )

    try:
        previous_audio_name = slide.speech_audio.name if slide.speech_audio else ''
        filename = f'slide-{slide.pk}-speech-{timezone.now().strftime("%Y%m%d-%H%M%S")}.mp3'
        slide.speech_audio.save(filename, ContentFile(result.audio_bytes), save=False)
        slide.speech_text = safe_speech_text
        slide.speech_voice_id = result.voice_id
        slide.speech_model_id = result.model_id
        slide.speech_output_format = result.output_format
        slide.speech_status = ReelProject.SPEECH_STATUS_READY
        slide.speech_error = ''
        slide.speech_generated_at = timezone.now()
        slide.save(
            update_fields=[
                'speech_audio',
                'speech_text',
                'speech_voice_id',
                'speech_model_id',
                'speech_output_format',
                'speech_status',
                'speech_error',
                'speech_generated_at',
                'updated_at',
            ]
        )
    except Exception as exc:
        raise TTSAPIError(f'Erreur lors de la sauvegarde audio: {exc}') from exc

    if previous_audio_name and previous_audio_name != slide.speech_audio.name:
        try:
            default_storage.delete(previous_audio_name)
        except Exception:
            pass

    slide._tts_result = result  # piggyback, used by views to surface stats in the response
    return slide


def _normalize_cta_text(value):
    raw_value = str(value or '').strip()
    if not raw_value or raw_value in LEGACY_CTA_TEXTS:
        return DEFAULT_CTA_TEXT

    raw_value = raw_value.replace('\\n', '\n')
    raw_value = re.sub(r'\s+\|\s+', '\n', raw_value)
    lines = [_normalize_line(line) for line in raw_value.splitlines()]
    lines = [line for line in lines if line]
    return '\n'.join(lines) or DEFAULT_CTA_TEXT


_SLIDE_TYPES = {
    ReelSlide.TYPE_HOOK,
    ReelSlide.TYPE_KATEX,
    ReelSlide.TYPE_CUMULATIVE_KATEX,
    ReelSlide.TYPE_RESULT,
    ReelSlide.TYPE_CTA,
}

_TEMPLATE_MARKER_PATTERN = re.compile(
    r'^\s*(HOOK|CTA|TEXT|QUESTION|TITLE|KATEX|VOICE|DURATION|TYPE)\s*:\s*(.*)\s*$',
    flags=re.IGNORECASE,
)
_SLIDE_HEADER_PATTERN = re.compile(
    r'^\s*SLIDE\s*(?P<index>\d+)\s*(?:[\|\-:]\s*)?(?P<slide_type>hook|katex|cumulative_katex|result|cta)?\s*$',
    flags=re.IGNORECASE,
)
_SLIDE_SEPARATOR_PATTERN = re.compile(r'^\s*(?:---+|===+)\s*$')
_INSTAGRAM_CAPTION_HEADER_PATTERN = re.compile(
    r'^\s*(?:INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM)\s*:\s*(.*)\s*$',
    flags=re.IGNORECASE,
)
_INSTAGRAM_CAPTION_END_PATTERN = re.compile(
    r'^\s*END_(?:INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM)\s*$',
    flags=re.IGNORECASE,
)


def _normalize_line(value):
    cleaned = str(value or '').strip()
    cleaned = re.sub(r'^\s*\d+[\)\.\-:]\s+', '', cleaned)
    cleaned = re.sub(r'^[•\*]\s+', '', cleaned)
    cleaned = re.sub(r'^\-\s+', '', cleaned)
    return cleaned.strip()


def _append_multiline(record, field_name, value):
    clean_value = str(value or '').strip()
    if not clean_value:
        return
    current = str(record.get(field_name) or '').strip()
    record[field_name] = f'{current}\n{clean_value}' if current else clean_value


def _extract_instagram_caption(template_text):
    kept_lines = []
    caption_lines = []
    capturing = False

    for raw_line in str(template_text or '').splitlines():
        line = str(raw_line or '').rstrip()
        stripped = line.strip()

        if capturing:
            if _INSTAGRAM_CAPTION_END_PATTERN.match(stripped):
                capturing = False
                continue
            if _SLIDE_HEADER_PATTERN.match(stripped):
                capturing = False
                kept_lines.append(line)
                continue
            caption_lines.append(line)
            continue

        caption_header = _INSTAGRAM_CAPTION_HEADER_PATTERN.match(stripped)
        if caption_header:
            capturing = True
            first_line = caption_header.group(1).strip()
            if first_line:
                caption_lines.append(first_line)
            continue

        kept_lines.append(line)

    caption = '\n'.join(caption_lines).strip()
    return '\n'.join(kept_lines).strip(), caption


def _parse_slide_type(raw_value):
    normalized = str(raw_value or '').strip().lower()
    alias_map = {
        'hook': ReelSlide.TYPE_HOOK,
        'intro': ReelSlide.TYPE_HOOK,
        'katex': ReelSlide.TYPE_KATEX,
        'math': ReelSlide.TYPE_KATEX,
        'cumulative': ReelSlide.TYPE_CUMULATIVE_KATEX,
        'cumulative_katex': ReelSlide.TYPE_CUMULATIVE_KATEX,
        'cumul_katex': ReelSlide.TYPE_CUMULATIVE_KATEX,
        'result': ReelSlide.TYPE_RESULT,
        'final': ReelSlide.TYPE_RESULT,
        'cta': ReelSlide.TYPE_CTA,
    }
    return alias_map.get(normalized, '')


def _normalize_katex_block(raw_value):
    content = str(raw_value or '').strip()
    if not content:
        return ''
    if '\\begin{' in content and '\\end{' in content:
        return content

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    if not lines:
        return ''
    if len(lines) == 1:
        return lines[0]
    return _to_aligned_katex(lines)


def _split_line_by_width(line, max_chars):
    clean_line = _normalize_line(line)
    if not clean_line:
        return []
    if len(clean_line) <= max_chars:
        return [clean_line]

    words = clean_line.split()
    if len(words) <= 1:
        return [clean_line[i:i + max_chars] for i in range(0, len(clean_line), max_chars)]

    chunks = []
    current = ''
    for word in words:
        candidate = word if not current else f'{current} {word}'
        if len(candidate) <= max_chars:
            current = candidate
            continue

        if current:
            chunks.append(current)
        if len(word) <= max_chars:
            current = word
        else:
            hard_chunks = [word[i:i + max_chars] for i in range(0, len(word), max_chars)]
            chunks.extend(hard_chunks[:-1])
            current = hard_chunks[-1]

    if current:
        chunks.append(current)
    return chunks


def _split_katex_line_by_width(line, max_chars):
    clean_line = _normalize_line(line)
    if not clean_line:
        return []
    if len(clean_line) <= max_chars:
        return [clean_line]

    safe_parts = re.split(r'\s*\\q?quad\s*', clean_line)
    safe_parts = [part.strip() for part in safe_parts if part.strip()]
    if len(safe_parts) > 1:
        return safe_parts

    return [clean_line]


def _build_slide_payload(
    *,
    slide_type,
    title='',
    screen_text='',
    katex='',
    voice_script='',
):
    normalized_type = _parse_slide_type(slide_type) or ReelSlide.TYPE_KATEX
    if normalized_type not in _SLIDE_TYPES:
        normalized_type = ReelSlide.TYPE_KATEX

    safe_title = str(title or '').strip()
    safe_screen_text = str(screen_text or '').strip()
    safe_katex = str(katex or '').strip()
    safe_voice = str(voice_script or '').strip()
    safe_duration = DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS

    safe_katex = _normalize_katex_block(safe_katex)

    return {
        'slide_type': normalized_type,
        'title': safe_title,
        'screen_text': safe_screen_text,
        'katex': safe_katex,
        'voice_script': safe_voice,
        'duration_seconds': safe_duration,
    }


def _append_katex_lines(record, value, max_chars):
    for line in _split_katex_line_by_width(value, max_chars):
        _append_multiline(record, 'katex', line)


def _parse_structured_template(template_text, max_chars):
    lines = str(template_text or '').splitlines()
    slides_raw = []
    current_slide = None
    has_structured_headers = False

    for raw_line in lines:
        line = str(raw_line or '').rstrip()
        stripped = line.strip()
        if not stripped:
            continue

        header_match = _SLIDE_HEADER_PATTERN.match(stripped)
        if header_match:
            has_structured_headers = True
            if current_slide:
                slides_raw.append(current_slide)

            header_index = int(header_match.group('index'))
            header_type = _parse_slide_type(header_match.group('slide_type') or '')
            current_slide = {
                '_order_hint': header_index,
                '_position': len(slides_raw),
                'slide_type': header_type or ReelSlide.TYPE_KATEX,
                'title': '',
                'screen_text': '',
                'katex': '',
                'voice_script': '',
            }
            continue

        if _SLIDE_SEPARATOR_PATTERN.match(stripped):
            if current_slide:
                slides_raw.append(current_slide)
                current_slide = None
            continue

        if not has_structured_headers or current_slide is None:
            continue

        marker_match = _TEMPLATE_MARKER_PATTERN.match(stripped)
        if marker_match:
            marker = marker_match.group(1).upper()
            value = marker_match.group(2).strip()

            if marker == 'TYPE':
                parsed_type = _parse_slide_type(value)
                if parsed_type:
                    current_slide['slide_type'] = parsed_type
            elif marker == 'DURATION':
                # Ignored in V1: real duration will come from voice generation in a later step.
                pass
            elif marker == 'TITLE':
                _append_multiline(current_slide, 'title', value)
            elif marker in {'TEXT', 'QUESTION', 'HOOK', 'CTA'}:
                if marker == 'HOOK':
                    current_slide['slide_type'] = ReelSlide.TYPE_HOOK
                if marker == 'CTA':
                    current_slide['slide_type'] = ReelSlide.TYPE_CTA
                _append_multiline(current_slide, 'screen_text', value)
            elif marker == 'KATEX':
                _append_katex_lines(current_slide, value, max_chars)
            elif marker == 'VOICE':
                _append_multiline(current_slide, 'voice_script', value)
            continue

        if current_slide['slide_type'] in {ReelSlide.TYPE_HOOK, ReelSlide.TYPE_CTA}:
            _append_multiline(current_slide, 'screen_text', stripped)
        else:
            _append_katex_lines(current_slide, stripped, max_chars)

    if current_slide:
        slides_raw.append(current_slide)

    if not has_structured_headers:
        return []

    slides_raw.sort(key=lambda slide: (slide.get('_order_hint', 10_000), slide.get('_position', 0)))

    slides = []
    for slide in slides_raw:
        payload = _build_slide_payload(
            slide_type=slide.get('slide_type'),
            title=slide.get('title', ''),
            screen_text=slide.get('screen_text', ''),
            katex=slide.get('katex', ''),
            voice_script=slide.get('voice_script', ''),
        )
        if payload['screen_text'] or payload['katex'] or payload['voice_script'] or payload['title']:
            slides.append(payload)
    return slides


def _parse_template(template_text):
    hook_text = ''
    cta_text = ''
    custom_title = ''
    raw_katex_lines = []
    raw_text_lines = []

    for raw in str(template_text or '').splitlines():
        cleaned = _normalize_line(raw)
        if not cleaned:
            continue

        marker_match = _TEMPLATE_MARKER_PATTERN.match(cleaned)
        if marker_match:
            marker = marker_match.group(1).upper()
            value = marker_match.group(2).strip()
            if marker == 'HOOK':
                hook_text = value
            elif marker == 'CTA':
                cta_text = value
            elif marker == 'TITLE':
                custom_title = value
            elif marker in {'TEXT', 'QUESTION'} and value:
                raw_text_lines.append(value)
            elif marker == 'KATEX' and value:
                raw_katex_lines.append(value)
            continue

        raw_katex_lines.append(cleaned)

    return {
        'hook_text': hook_text,
        'cta_text': cta_text,
        'title': custom_title,
        'katex_lines': raw_katex_lines,
        'text_lines': raw_text_lines,
    }


def _to_aligned_katex(lines):
    normalized = []
    for line in lines:
        clean_line = _normalize_line(line)
        if not clean_line:
            continue
        if not clean_line.startswith('&'):
            clean_line = f'&{clean_line}'
        normalized.append(clean_line)

    if not normalized:
        return ''

    return '\\begin{aligned}\n' + '\\\\[0.4em]\n'.join(normalized) + '\n\\end{aligned}'


def _build_template_slides(project, payload):
    template_text, _ = _extract_instagram_caption(payload['template_text'])
    max_chars = int(payload['max_chars_per_line'])
    structured_slides = _parse_structured_template(template_text, max_chars)
    if structured_slides:
        return structured_slides
    if any(_SLIDE_HEADER_PATTERN.match(line.strip()) for line in str(template_text or '').splitlines() if line.strip()):
        return []

    parsed = _parse_template(template_text)
    include_hook_input = payload.get('include_hook')
    include_cta_input = payload.get('include_cta')

    katex_lines = []
    for raw in parsed['katex_lines']:
        katex_lines.extend(_split_katex_line_by_width(raw, max_chars))

    text_lines = []
    for raw in parsed['text_lines']:
        text_lines.extend(_split_line_by_width(raw, max_chars))

    has_katex = len(katex_lines) > 0
    has_text = len(text_lines) > 0
    if not has_katex and not has_text:
        return []

    # Auto mode: if include flags are not explicitly provided,
    # hook/cta are inferred from HOOK:/CTA: markers in template text.
    include_hook = bool(parsed['hook_text']) if include_hook_input is None else bool(include_hook_input)
    include_cta = bool(parsed['cta_text']) if include_cta_input is None else bool(include_cta_input)

    slides_payload = []

    if include_hook:
        hook_value = payload.get('hook_text') or parsed['hook_text'] or 'Défi maths OptiTAB'
        hook_katex = katex_lines.pop(0) if katex_lines else ''
        hook_question = text_lines.pop(0) if text_lines else ''
        slides_payload.append({
            'slide_type': ReelSlide.TYPE_HOOK,
            'title': hook_value,
            'screen_text': hook_question,
            'katex': _normalize_katex_block(hook_katex),
            'voice_script': '',
            'duration_seconds': DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS,
        })

    has_katex = len(katex_lines) > 0
    has_text = len(text_lines) > 0
    if not has_katex and not has_text:
        return slides_payload

    total_steps = max(len(katex_lines), len(text_lines))
    cumulative_katex = []
    cumulative_text = []
    step_title = parsed['title'] or project.title or 'Étapes'

    for index in range(total_steps):
        if index < len(katex_lines):
            cumulative_katex.append(katex_lines[index])
        if index < len(text_lines):
            cumulative_text.append(text_lines[index])

        if index == 0:
            slide_type = ReelSlide.TYPE_KATEX if has_katex else ReelSlide.TYPE_CUMULATIVE_KATEX
        elif index == total_steps - 1:
            slide_type = ReelSlide.TYPE_RESULT
        else:
            slide_type = ReelSlide.TYPE_CUMULATIVE_KATEX

        slide_title = 'Résultat' if slide_type == ReelSlide.TYPE_RESULT else step_title
        slides_payload.append({
            'slide_type': slide_type,
            'title': slide_title,
            'screen_text': '\n'.join(cumulative_text),
            'katex': _to_aligned_katex(cumulative_katex),
            'voice_script': '',
            'duration_seconds': DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS,
        })

    if include_cta:
        cta_value = _normalize_cta_text(payload.get('cta_text') or parsed['cta_text'])
        cta_katex = _normalize_katex_block(katex_lines[-1]) if katex_lines else ''
        slides_payload.append({
            'slide_type': ReelSlide.TYPE_CTA,
            'title': 'Résultat' if cta_katex else '',
            'screen_text': cta_value,
            'katex': cta_katex,
            'voice_script': '',
            'duration_seconds': DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS,
        })

    return slides_payload


class ReelProjectListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request):
        queryset = ReelProject.objects.all().order_by('-updated_at', '-created_at')
        serializer = ReelProjectSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ReelProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        detail_serializer = _project_serializer(project, request, detail=True)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ReelProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request, pk):
        project = get_object_or_404(ReelProject.objects.prefetch_related('slides'), pk=pk)
        serializer = _project_serializer(project, request, detail=True)
        return Response(serializer.data)

    def patch(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        serializer = ReelProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_project = serializer.save()
        detail_serializer = _project_serializer(updated_project, request, detail=True)
        return Response(detail_serializer.data)

    def delete(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ReelProjectGenerateDemoSlidesView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)

        with transaction.atomic():
            _clear_project_speech(project)
            _clear_project_video(project)
            project.slides.all().delete()

            slides_to_create = []
            for index, payload in enumerate(DEMO_SLIDES, start=1):
                slides_to_create.append(
                    ReelSlide(
                        reel_project=project,
                        order=index,
                        slide_type=payload['slide_type'],
                        title=payload.get('title', ''),
                        screen_text=payload.get('screen_text', ''),
                        katex=payload.get('katex', ''),
                        voice_script=payload.get('voice_script', ''),
                        duration_seconds=payload.get('duration_seconds', 4),
                        layout_status=ReelSlide.LAYOUT_UNCHECKED,
                        layout_notes='',
                    )
                )

            ReelSlide.objects.bulk_create(slides_to_create)

            project.slide_count = len(slides_to_create)
            project.status = ReelProject.STATUS_DRAFT
            project.instagram_caption = ''
            project.save(update_fields=['slide_count', 'status', 'instagram_caption', 'updated_at'])

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        serializer = _project_serializer(project, request, detail=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReelProjectGenerateFromTemplateView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        serializer = ReelTemplateGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        clean_template_text, instagram_caption = _extract_instagram_caption(
            serializer.validated_data['template_text']
        )
        template_payload = {
            **serializer.validated_data,
            'template_text': clean_template_text,
        }
        slides_payload = _build_template_slides(project, template_payload)
        if not slides_payload:
            return Response(
                {'detail': "Aucune ligne exploitable trouvée dans le template."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            _clear_project_speech(project)
            _clear_project_video(project)
            project.slides.all().delete()

            slides_to_create = []
            for index, payload in enumerate(slides_payload, start=1):
                slides_to_create.append(
                    ReelSlide(
                        reel_project=project,
                        order=index,
                        slide_type=payload['slide_type'],
                        title=payload.get('title', ''),
                        screen_text=payload.get('screen_text', ''),
                        katex=payload.get('katex', ''),
                        voice_script=payload.get('voice_script', ''),
                        duration_seconds=payload.get('duration_seconds', 4),
                        layout_status=ReelSlide.LAYOUT_UNCHECKED,
                        layout_notes='',
                    )
                )

            ReelSlide.objects.bulk_create(slides_to_create)

            project.slide_count = len(slides_to_create)
            project.status = ReelProject.STATUS_DRAFT
            project.instagram_caption = instagram_caption
            project.save(update_fields=['slide_count', 'status', 'instagram_caption', 'updated_at'])

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(_project_serializer(project, request, detail=True).data, status=status.HTTP_201_CREATED)


def _update_project_slides_from_template(project, slides_payload):
    existing_slides = list(project.slides.select_for_update().order_by('order', 'id'))
    changed = False

    for index, payload in enumerate(slides_payload, start=1):
        slide = existing_slides[index - 1] if index - 1 < len(existing_slides) else None
        if slide is None:
            ReelSlide.objects.create(
                reel_project=project,
                order=index,
                slide_type=payload['slide_type'],
                title=payload.get('title', ''),
                screen_text=payload.get('screen_text', ''),
                katex=payload.get('katex', ''),
                voice_script=payload.get('voice_script', ''),
                duration_seconds=payload.get('duration_seconds', DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS),
                layout_status=ReelSlide.LAYOUT_UNCHECKED,
                layout_notes='',
            )
            changed = True
            continue

        previous_speech_text = build_slide_speech_text(slide)
        update_fields = []
        field_values = {
            'order': index,
            'slide_type': payload['slide_type'],
            'title': payload.get('title', ''),
            'screen_text': payload.get('screen_text', ''),
            'katex': payload.get('katex', ''),
            'voice_script': payload.get('voice_script', ''),
            'duration_seconds': payload.get('duration_seconds', DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS),
        }

        for field_name, field_value in field_values.items():
            if getattr(slide, field_name) != field_value:
                setattr(slide, field_name, field_value)
                update_fields.append(field_name)

        content_changed = any(
            field_name in update_fields
            for field_name in ('slide_type', 'title', 'screen_text', 'katex', 'voice_script', 'duration_seconds')
        )
        if content_changed:
            slide.layout_status = ReelSlide.LAYOUT_UNCHECKED
            slide.layout_notes = ''
            update_fields.extend(['layout_status', 'layout_notes'])

        if update_fields:
            slide.save(update_fields=[*update_fields, 'updated_at'])
            changed = True

        if build_slide_speech_text(slide) != previous_speech_text:
            _clear_slide_speech(slide)

    for slide in existing_slides[len(slides_payload):]:
        _clear_slide_speech(slide)
        slide.delete()
        changed = True

    return changed


class ReelProjectSaveTemplateView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        serializer = ReelTemplateGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        clean_template_text, instagram_caption = _extract_instagram_caption(
            serializer.validated_data['template_text']
        )
        template_payload = {
            **serializer.validated_data,
            'template_text': clean_template_text,
        }
        slides_payload = _build_template_slides(project, template_payload)
        if not slides_payload:
            return Response(
                {'detail': "Aucune ligne exploitable trouvee dans le template."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            project = ReelProject.objects.select_for_update().get(pk=project.pk)
            slides_changed = _update_project_slides_from_template(project, slides_payload)
            video_should_clear = slides_changed or project.slide_count != len(slides_payload)
            project_changed = (
                project.slide_count != len(slides_payload)
                or project.status != ReelProject.STATUS_DRAFT
                or project.instagram_caption != instagram_caption
            )
            project.slide_count = len(slides_payload)
            project.status = ReelProject.STATUS_DRAFT
            project.instagram_caption = instagram_caption
            if project_changed:
                project.save(update_fields=['slide_count', 'status', 'instagram_caption', 'updated_at'])

            project = _sync_project_speech_from_slides(project.pk)
            if video_should_clear:
                _clear_project_video(project)

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(_project_serializer(project, request, detail=True).data)


class ReelProjectGenerateSpeechView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject.objects.prefetch_related('slides'), pk=pk)
        serializer = ReelSpeechGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        requested_text = str(serializer.validated_data.get('text') or '').strip()
        speech_text = requested_text or build_project_speech_text(project)
        if not speech_text:
            return Response(
                {'detail': 'Aucun texte voix disponible pour ce reel.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project.speech_status = ReelProject.SPEECH_STATUS_EMPTY
        project.speech_error = ''
        project.save(update_fields=['speech_status', 'speech_error', 'updated_at'])

        try:
            tts_result = tts_generate_speech(
                text=speech_text,
                provider=serializer.validated_data.get('provider', ''),
                voice_id=serializer.validated_data.get('voice_id', ''),
                model_id=serializer.validated_data.get('model_id', ''),
                output_format=serializer.validated_data.get('output_format', ''),
            )
        except ValueError as exc:
            project.speech_status = ReelProject.SPEECH_STATUS_ERROR
            project.speech_error = str(exc)
            project.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except TTSConfigurationError as exc:
            project.speech_status = ReelProject.SPEECH_STATUS_ERROR
            project.speech_error = str(exc)
            project.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except TTSQuotaExceeded as exc:
            project.speech_status = ReelProject.SPEECH_STATUS_ERROR
            project.speech_error = str(exc)
            project.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except TTSAPIError as exc:
            project.speech_status = ReelProject.SPEECH_STATUS_ERROR
            project.speech_error = str(exc)
            project.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        tts_logger.info(
            'Project speech generated | project_id=%s | provider=%s | voice=%s | chars=%d | cached=%s',
            project.pk, tts_result.provider, tts_result.voice_id,
            tts_result.character_count, tts_result.cached,
        )

        previous_audio_name = project.speech_audio.name if project.speech_audio else ''
        filename = f'reel-{project.pk}-speech-{timezone.now().strftime("%Y%m%d-%H%M%S")}.mp3'
        project.speech_audio.save(filename, ContentFile(tts_result.audio_bytes), save=False)
        project.speech_text = speech_text
        project.speech_voice_id = tts_result.voice_id
        project.speech_model_id = tts_result.model_id
        project.speech_output_format = tts_result.output_format
        project.speech_status = ReelProject.SPEECH_STATUS_READY
        project.speech_error = ''
        project.speech_generated_at = timezone.now()
        project.save(
            update_fields=[
                'speech_audio',
                'speech_text',
                'speech_voice_id',
                'speech_model_id',
                'speech_output_format',
                'speech_status',
                'speech_error',
                'speech_generated_at',
                'updated_at',
            ]
        )

        if previous_audio_name and previous_audio_name != project.speech_audio.name:
            try:
                default_storage.delete(previous_audio_name)
            except Exception:
                pass

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(
            {
                'project': _project_serializer(project, request, detail=True).data,
                'speech': {
                    'status': project.speech_status,
                    'audio_url': _project_serializer(project, request).data.get('speech_audio_url'),
                    'text_length': len(speech_text),
                    'character_count': tts_result.character_count,
                    'cached': tts_result.cached,
                    'provider': tts_result.provider,
                    'generated_at': project.speech_generated_at,
                    'voice_id': project.speech_voice_id,
                    'model_id': project.speech_model_id,
                    'output_format': project.speech_output_format,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ReelVoiceListView(APIView):
    """Return the available TTS providers and their voices.

    Backwards compatible: still exposes ``voices`` + ``default_voice_id`` (the
    historical ElevenLabs-only payload) at the top level when requested with
    ``?provider=elevenlabs``. By default, returns the multi-provider payload
    used by the new frontend dropdowns.
    """
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request):
        provider_filter = str(request.query_params.get('provider') or '').strip().lower()

        # Legacy single-provider mode (kept for compatibility with old clients).
        if provider_filter == PROVIDER_ELEVENLABS or request.query_params.get('legacy') == '1':
            language = str(request.query_params.get('language') or 'fr').strip().lower()
            accent = str(request.query_params.get('accent') or 'parisian').strip().lower()
            try:
                voices = list_filtered_voices(language=language, accent=accent, include_fallback=True)
            except ElevenLabsConfigurationError as exc:
                return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except ElevenLabsAPIError as exc:
                return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)
            return Response(
                {
                    'voices': voices,
                    'default_voice_id': getattr(settings, 'ELEVENLABS_VOICE_ID', ''),
                    'filters': {'language': language, 'accent': accent},
                }
            )

        payload = list_providers_payload()

        # Also include a flat ``voices`` array for the *default* provider so that
        # legacy clients that ignore the ``providers`` field keep working.
        default_provider_id = payload['default_provider']
        default_provider_payload = next(
            (p for p in payload['providers'] if p['id'] == default_provider_id),
            None,
        )
        if default_provider_payload:
            payload['voices'] = default_provider_payload.get('voices', [])
            payload['default_voice_id'] = default_provider_payload.get('default_voice_id', '')
        else:
            payload['voices'] = []
            payload['default_voice_id'] = ''

        return Response(payload)


class ReelTTSTestVoiceView(APIView):
    """Generate a short audio preview for a given provider+voice.

    Returns ``audio/mpeg`` bytes directly so the frontend can play it via an
    ``<audio>`` element without going through storage.
    """
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request):
        serializer = ReelTTSTestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            result = tts_generate_speech(
                text=serializer.validated_data['text'],
                provider=serializer.validated_data.get('provider', ''),
                voice_id=serializer.validated_data.get('voice_id', ''),
                use_cache=True,
            )
        except ValueError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except TTSConfigurationError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except TTSQuotaExceeded as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except TTSAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        tts_logger.info(
            'TTS test preview | provider=%s | voice=%s | chars=%d | cached=%s',
            result.provider, result.voice_id, result.character_count, result.cached,
        )

        response = HttpResponse(result.audio_bytes, content_type='audio/mpeg')
        response['X-TTS-Provider'] = result.provider
        response['X-TTS-Voice-Id'] = result.voice_id
        response['X-TTS-Character-Count'] = str(result.character_count)
        response['X-TTS-Cached'] = '1' if result.cached else '0'
        return response


class ReelProjectGenerateSlideSpeechesView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject.objects.prefetch_related('slides'), pk=pk)
        serializer = ReelSpeechGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        generated_count = 0
        skipped_count = 0
        cached_count = 0
        total_characters = 0
        last_provider = ''

        for slide in project.slides.all().order_by('order', 'id'):
            speech_text = build_slide_speech_text(slide)
            if not speech_text:
                _clear_slide_speech(slide)
                skipped_count += 1
                continue

            try:
                _generate_and_save_slide_speech(
                    slide,
                    speech_text=speech_text,
                    provider=serializer.validated_data.get('provider', ''),
                    voice_id=serializer.validated_data.get('voice_id', ''),
                    model_id=serializer.validated_data.get('model_id', ''),
                    output_format=serializer.validated_data.get('output_format', ''),
                )
                generated_count += 1
                tts_meta = getattr(slide, '_tts_result', None)
                if tts_meta is not None:
                    total_characters += tts_meta.character_count
                    last_provider = tts_meta.provider
                    if tts_meta.cached:
                        cached_count += 1
            except ValueError as exc:
                slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
                slide.speech_error = str(exc)
                slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
                return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
            except TTSConfigurationError as exc:
                slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
                slide.speech_error = str(exc)
                slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
                return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except TTSQuotaExceeded as exc:
                slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
                slide.speech_error = str(exc)
                slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
                return Response({'detail': str(exc)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
            except TTSAPIError as exc:
                slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
                slide.speech_error = str(exc)
                slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
                return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        project = _sync_project_speech_from_slides(project.pk)
        _clear_project_video(project)
        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(
            {
                'project': _project_serializer(project, request, detail=True).data,
                'speech': {
                    'generated_count': generated_count,
                    'skipped_count': skipped_count,
                    'cached_count': cached_count,
                    'character_count': total_characters,
                    'provider': last_provider,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ReelProjectExportVideoView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject.objects.prefetch_related('slides'), pk=pk)
        serializer = ReelVideoExportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            project.video_status = ReelProject.VIDEO_STATUS_EMPTY
            project.video_error = ''
            project.save(update_fields=['video_status', 'video_error', 'updated_at'])
        except Exception as exc:
            import traceback as _tb
            return Response(
                {'detail': f'DB init error: {type(exc).__name__}: {exc}\n{_tb.format_exc()}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        audio_issues = _collect_video_export_audio_issues(project, serializer.validated_data['frames'])
        if audio_issues:
            detail = 'Export MP4 bloque: regenere les MP3 des slides avant l export. ' + ' '.join(audio_issues[:6])
            if len(audio_issues) > 6:
                detail += f' (+{len(audio_issues) - 6} autres)'
            project.video_status = ReelProject.VIDEO_STATUS_ERROR
            project.video_error = detail[:2000]
            project.save(update_fields=['video_status', 'video_error', 'updated_at'])
            return Response(
                {
                    'detail': detail,
                    'issues': audio_issues,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            generated = export_reel_video(
                project,
                serializer.validated_data['frames'],
                width=serializer.validated_data.get('width', 1080),
                height=serializer.validated_data.get('height', 1920),
                fps=serializer.validated_data.get('fps', 30),
                crf=serializer.validated_data.get('crf', 18),
                preset=serializer.validated_data.get('preset', 'veryfast'),
            )
        except VideoExportConfigurationError as exc:
            project.video_status = ReelProject.VIDEO_STATUS_ERROR
            project.video_error = str(exc)
            project.save(update_fields=['video_status', 'video_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except VideoExportError as exc:
            project.video_status = ReelProject.VIDEO_STATUS_ERROR
            project.video_error = str(exc)
            project.save(update_fields=['video_status', 'video_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:
            import traceback as _tb
            detail = f'{type(exc).__name__}: {exc}\n{_tb.format_exc()}'
            project.video_status = ReelProject.VIDEO_STATUS_ERROR
            project.video_error = detail[:2000]
            try:
                project.save(update_fields=['video_status', 'video_error', 'updated_at'])
            except Exception:
                pass
            return Response({'detail': detail}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            previous_video_name = project.video_file.name if project.video_file else ''
            filename = f'reel-{project.pk}-video-{timezone.now().strftime("%Y%m%d-%H%M%S")}.mp4'
            project.video_file.save(filename, ContentFile(generated['video_bytes']), save=False)
            project.video_status = ReelProject.VIDEO_STATUS_READY
            project.video_error = ''
            project.video_generated_at = timezone.now()
            project.video_width = generated['width']
            project.video_height = generated['height']
            project.video_fps = generated['fps']
            project.save(
                update_fields=[
                    'video_file',
                    'video_status',
                    'video_error',
                    'video_generated_at',
                    'video_width',
                    'video_height',
                    'video_fps',
                    'updated_at',
                ]
            )
        except Exception as exc:
            project.video_status = ReelProject.VIDEO_STATUS_ERROR
            project.video_error = str(exc)
            try:
                project.save(update_fields=['video_status', 'video_error', 'updated_at'])
            except Exception:
                pass
            return Response(
                {'detail': f'Erreur lors de la sauvegarde de la vidéo: {exc}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if previous_video_name and previous_video_name != project.video_file.name:
            try:
                default_storage.delete(previous_video_name)
            except Exception:
                pass

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        project_data = _project_serializer(project, request, detail=True).data
        return Response(
            {
                'project': project_data,
                'video': {
                    'status': project.video_status,
                    'url': project_data.get('video_file_url'),
                    'generated_at': project.video_generated_at,
                    'frame_count': generated['frame_count'],
                    'width': project.video_width,
                    'height': project.video_height,
                    'fps': project.video_fps,
                    'crf': generated['crf'],
                    'preset': generated['preset'],
                },
            },
            status=status.HTTP_201_CREATED,
        )


class ReelProjectDownloadVideoView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]
    renderer_classes = [JSONRenderer]
    content_negotiation_class = ReelDownloadContentNegotiation

    def get(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        if not project.video_file:
            return Response(
                {'detail': 'Aucune video MP4 disponible pour ce reel.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            project.video_file.open('rb')
        except (FileNotFoundError, OSError, ValueError):
            return Response(
                {'detail': 'Le fichier video MP4 est introuvable.'},
                status=status.HTTP_404_NOT_FOUND,
            )

        return FileResponse(
            project.video_file,
            as_attachment=True,
            filename=_project_video_download_filename(project),
            content_type='video/mp4',
        )


class ReelSlideGenerateSpeechView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        slide = get_object_or_404(ReelSlide.objects.select_related('reel_project'), pk=pk)
        serializer = ReelSpeechGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        requested_text = str(serializer.validated_data.get('text') or '').strip()
        speech_text = requested_text or build_slide_speech_text(slide)

        try:
            slide = _generate_and_save_slide_speech(
                slide,
                speech_text=speech_text,
                provider=serializer.validated_data.get('provider', ''),
                voice_id=serializer.validated_data.get('voice_id', ''),
                model_id=serializer.validated_data.get('model_id', ''),
                output_format=serializer.validated_data.get('output_format', ''),
            )
        except ValueError as exc:
            slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
            slide.speech_error = str(exc)
            slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except TTSConfigurationError as exc:
            slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
            slide.speech_error = str(exc)
            slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except TTSQuotaExceeded as exc:
            slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
            slide.speech_error = str(exc)
            slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except TTSAPIError as exc:
            slide.speech_status = ReelProject.SPEECH_STATUS_ERROR
            slide.speech_error = str(exc)
            slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        project = _sync_project_speech_from_slides(slide.reel_project_id)
        _clear_project_video(project)
        slide_payload = _slide_serializer(slide, request).data
        slide_payload['project'] = _project_serializer(project, request).data
        tts_meta = getattr(slide, '_tts_result', None)
        if tts_meta is not None:
            slide_payload['_tts'] = {
                'provider': tts_meta.provider,
                'character_count': tts_meta.character_count,
                'cached': tts_meta.cached,
            }
        return Response(slide_payload, status=status.HTTP_201_CREATED)


class ReelSlideDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def patch(self, request, pk):
        slide = get_object_or_404(ReelSlide.objects.select_related('reel_project'), pk=pk)
        previous_speech_text = build_slide_speech_text(slide)
        serializer = ReelSlideSerializer(slide, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_slide = serializer.save()
        if build_slide_speech_text(updated_slide) != previous_speech_text:
            _clear_slide_speech(updated_slide)
            project = _sync_project_speech_from_slides(updated_slide.reel_project_id)
        else:
            project = updated_slide.reel_project
            _touch_project(updated_slide.reel_project_id)
        _clear_project_video(project)
        slide_payload = _slide_serializer(updated_slide, request).data
        slide_payload['project'] = _project_serializer(project, request).data
        return Response(slide_payload)

    def delete(self, request, pk):
        slide = get_object_or_404(ReelSlide.objects.select_related('reel_project'), pk=pk)
        project_id = slide.reel_project_id
        project = slide.reel_project
        slide.delete()

        slide_count = ReelSlide.objects.filter(reel_project_id=project_id).count()
        ReelProject.objects.filter(pk=project_id).update(
            slide_count=slide_count,
            updated_at=timezone.now(),
        )
        project = _sync_project_speech_from_slides(project_id)
        _clear_project_video(project)
        return Response(status=status.HTTP_204_NO_CONTENT)
