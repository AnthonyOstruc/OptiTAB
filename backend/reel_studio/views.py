import json
import logging
import re
import uuid
from io import BytesIO
from decimal import Decimal

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models import Sum
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
from PIL import Image, ImageOps, UnidentifiedImageError

from .models import GeminiUsageLog, ReelProject, ReelSlide
from .permissions import IsStaffOrSuperuser
from .serializers import (
    ReelGeminiCarouselGenerateSerializer,
    ReelProjectDetailSerializer,
    ReelProjectSerializer,
    ReelSlideSerializer,
    ReelSpeechGenerateSerializer,
    ReelTTSTestSerializer,
    ReelTemplateGenerateSerializer,
    ReelVideoExportSerializer,
)
from .gemini import (
    GeminiAPIError,
    GeminiConfigurationError,
    IMAGE_INSTRUCTIONS_MAX_LENGTH,
    generate_carousel_image,
    generate_carousel_template,
    list_gemini_models,
    read_image_instructions,
    write_image_instructions,
)
from .elevenlabs import (
    ElevenLabsAPIError,
    ElevenLabsConfigurationError,
    build_slide_speech_text,
    build_project_speech_text,
    force_align_speech,
    generate_speech_mp3,
    list_filtered_voices,
    list_shared_voices,
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

    if _project_is_carousel(project):
        _clear_project_speech(project)
        return project

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


def _apply_pronunciation_overrides(text, overrides, *, base_language='fr'):
    safe_text = str(text or '')
    if not safe_text or not overrides:
        return safe_text

    safe_base_language = str(base_language or 'fr').strip().lower() or 'fr'

    sorted_overrides = sorted(
        (o for o in overrides if isinstance(o, dict)),
        key=lambda o: len(str(o.get('word') or '')),
        reverse=True,
    )

    for override in sorted_overrides:
        word = str(override.get('word') or '').strip()
        pronunciation = str(override.get('pronunciation') or '').strip()
        if not word or not pronunciation:
            continue

        language = str(override.get('language') or safe_base_language).strip().lower() or safe_base_language
        if language != safe_base_language:
            replacement = f', {pronunciation}, '
        else:
            replacement = pronunciation

        pattern = re.compile(rf'(?<!\w){re.escape(word)}(?!\w)', re.IGNORECASE)
        safe_text = pattern.sub(replacement, safe_text)

    safe_text = re.sub(r'\s+', ' ', safe_text).strip()
    safe_text = re.sub(r'\s+,', ',', safe_text)
    return safe_text


def _generate_and_save_slide_speech(
    slide,
    *,
    speech_text,
    provider='',
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
    google_speaking_rate=None,
    google_pitch=None,
    google_volume_gain_db=None,
    google_effects_profile_id='',
):
    safe_speech_text = str(speech_text or '').strip()
    if not safe_speech_text:
        raise ValueError('Aucun texte voix disponible pour cette slide.')

    overrides = []
    project = getattr(slide, 'reel_project', None)
    if project is not None:
        global_overrides = list(getattr(project, 'pronunciation_overrides', None) or [])
        by_voice = getattr(project, 'pronunciation_overrides_by_voice', None) or {}
        voice_overrides = list(by_voice.get(str(voice_id or '').strip(), []))
        voice_words_lower = {str(o.get('word') or '').lower() for o in voice_overrides}
        overrides = voice_overrides + [o for o in global_overrides if str(o.get('word') or '').lower() not in voice_words_lower]
    tts_text = _apply_pronunciation_overrides(safe_speech_text, overrides)

    slide.speech_status = ReelProject.SPEECH_STATUS_EMPTY
    slide.speech_error = ''
    slide.save(update_fields=['speech_status', 'speech_error', 'updated_at'])

    result = tts_generate_speech(
        text=tts_text,
        provider=provider,
        voice_id=voice_id,
        model_id=model_id,
        output_format=output_format,
        stability=stability,
        similarity_boost=similarity_boost,
        style=style,
        speed=speed,
        use_speaker_boost=use_speaker_boost,
        language_code=language_code,
        apply_text_normalization=apply_text_normalization,
        google_speaking_rate=google_speaking_rate,
        google_pitch=google_pitch,
        google_volume_gain_db=google_volume_gain_db,
        google_effects_profile_id=google_effects_profile_id,
    )

    tts_logger.info(
        'Slide speech generated | slide_id=%s | provider=%s | voice=%s | chars=%d | cached=%s',
        slide.pk,
        result.provider,
        result.voice_id,
        result.character_count,
        result.cached,
    )

    word_timings_payload = None
    try:
        alignment = force_align_speech(audio_bytes=result.audio_bytes, text=safe_speech_text)
        if alignment and alignment.get('words'):
            word_timings_payload = {
                'words': alignment['words'],
                'text': safe_speech_text,
                'aligned_at': timezone.now().isoformat(),
            }
    except (ElevenLabsAPIError, ElevenLabsConfigurationError, ValueError) as align_exc:
        tts_logger.warning(
            'Slide speech alignment failed | slide_id=%s | error=%s',
            slide.pk,
            align_exc,
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
        slide.speech_word_timings = word_timings_payload
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
                'speech_word_timings',
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


def _speech_generation_kwargs(validated_data):
    return {
        'provider': validated_data.get('provider', ''),
        'voice_id': validated_data.get('voice_id', ''),
        'model_id': validated_data.get('model_id', ''),
        'output_format': validated_data.get('output_format', ''),
        'stability': validated_data.get('stability'),
        'similarity_boost': validated_data.get('similarity_boost'),
        'style': validated_data.get('style'),
        'speed': validated_data.get('speed'),
        'use_speaker_boost': validated_data.get('use_speaker_boost'),
        'language_code': validated_data.get('language_code', ''),
        'apply_text_normalization': validated_data.get('apply_text_normalization', ''),
        'google_speaking_rate': validated_data.get('google_speaking_rate'),
        'google_pitch': validated_data.get('google_pitch'),
        'google_volume_gain_db': validated_data.get('google_volume_gain_db'),
        'google_effects_profile_id': validated_data.get('google_effects_profile_id', ''),
    }


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

_VISUAL_MARKERS = {'VISUAL', 'VISUEL', 'IMAGE', 'IMAGE_PROMPT'}

_TEMPLATE_MARKER_PATTERN = re.compile(
    r'^\s*(HOOK|CTA|TEXT|QUESTION|TITLE|KATEX|VOICE|DURATION|TYPE|VISUAL|VISUEL|IMAGE|IMAGE_PROMPT)\s*:\s*(.*)\s*$',
    flags=re.IGNORECASE,
)
_SLIDE_HEADER_PATTERN = re.compile(
    r'^\s*SLIDE\s*(?P<index>\d+)\s*'
    r'(?:[\|\-:]\s*(?P<slide_type>hook|katex|cumulative_katex|result|cta))?'
    r'(?:\s*\|\s*[A-Za-z0-9_\-]+)*\s*$',
    flags=re.IGNORECASE,
)
_SLIDE_SEPARATOR_PATTERN = re.compile(r'^\s*(?:---+|===+)\s*$')
_SPLIT_ZONE_PATTERN = re.compile(
    r'^\s*(?P<zone>LEFT|RIGHT|LABEL)\b\s*(?P<repeat>\(\s*repeat\s*\))?\s*:?\s*(?P<value>.*)$',
    flags=re.IGNORECASE,
)
_INSTAGRAM_CAPTION_HEADER_PATTERN = re.compile(
    r'^\s*(?:INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM|YOUTUBE_DESCRIPTION|DESCRIPTION_YOUTUBE|CAROUSEL_DESCRIPTION|DESCRIPTION_CAROUSEL|SOCIAL_DESCRIPTION|DESCRIPTION_SOCIAL)\s*:\s*(.*)\s*$',
    flags=re.IGNORECASE,
)
_INSTAGRAM_CAPTION_END_PATTERN = re.compile(
    r'^\s*END_(?:INSTAGRAM_DESCRIPTION|DESCRIPTION_INSTAGRAM|INSTAGRAM_CAPTION|CAPTION_INSTAGRAM|INSTAGRAM|YOUTUBE_DESCRIPTION|DESCRIPTION_YOUTUBE|CAROUSEL_DESCRIPTION|DESCRIPTION_CAROUSEL|SOCIAL_DESCRIPTION|DESCRIPTION_SOCIAL)\s*$',
    flags=re.IGNORECASE,
)


def _normalize_line(value):
    cleaned = str(value or '').strip()
    cleaned = re.sub(r'^\s*\d+[\)\.\-:]\s+', '', cleaned)
    cleaned = re.sub(r'^[•\*]\s+', '', cleaned)
    cleaned = re.sub(r'^\-\s+', '', cleaned)
    return cleaned.strip()


def _template_screen_text_for_slide(slide_type, text_lines):
    if slide_type == ReelSlide.TYPE_RESULT:
        return ''
    return '\n'.join(text_lines)


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
    layout_notes='',
    visual_prompt='',
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

    safe_layout_notes = str(layout_notes or '').strip()
    safe_visual_prompt = str(visual_prompt or '').strip()
    if safe_visual_prompt:
        layout_meta = {}
        if safe_layout_notes:
            try:
                parsed_layout = json.loads(safe_layout_notes)
                if isinstance(parsed_layout, dict):
                    layout_meta.update(parsed_layout)
            except (TypeError, ValueError):
                layout_meta['notes'] = safe_layout_notes
        layout_meta['visual_prompt'] = safe_visual_prompt
        safe_layout_notes = json.dumps(layout_meta, ensure_ascii=False)

    return {
        'slide_type': normalized_type,
        'title': safe_title,
        'screen_text': safe_screen_text,
        'katex': safe_katex,
        'voice_script': safe_voice,
        'duration_seconds': safe_duration,
        'layout_notes': safe_layout_notes,
    }


def _append_katex_lines(record, value, max_chars):
    for line in _split_katex_line_by_width(value, max_chars):
        _append_multiline(record, 'katex', line)


def _parse_structured_template(template_text, max_chars):
    lines = str(template_text or '').splitlines()
    slides_raw = []
    current_slide = None
    has_structured_headers = False
    last_right_block = None

    def begin_split_state(slide_dict, is_split):
        slide_dict['_split'] = bool(is_split)
        slide_dict['_zone'] = 'left'
        slide_dict['_right_label'] = ''
        slide_dict['_right_katex'] = []
        slide_dict['_right_repeat'] = False

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
            is_split = bool(re.search(r'\bsplit\b', stripped, flags=re.IGNORECASE))
            is_method = bool(re.search(r'\bmethod\b', stripped, flags=re.IGNORECASE))
            current_slide = {
                '_order_hint': header_index,
                '_position': len(slides_raw),
                'slide_type': header_type or ReelSlide.TYPE_KATEX,
                'title': '',
                'screen_text': '',
                'katex': '',
                'voice_script': '',
                '_method': is_method,
            }
            begin_split_state(current_slide, is_split)
            continue

        if _SLIDE_SEPARATOR_PATTERN.match(stripped):
            if current_slide:
                slides_raw.append(current_slide)
                current_slide = None
            continue

        if not has_structured_headers or current_slide is None:
            continue

        zone_match = _SPLIT_ZONE_PATTERN.match(stripped)
        if zone_match:
            zone_kind = zone_match.group('zone').upper()
            zone_repeat = bool(zone_match.group('repeat'))
            zone_value = zone_match.group('value').strip()
            if zone_kind == 'LEFT':
                current_slide['_zone'] = 'left'
            elif zone_kind == 'RIGHT':
                current_slide['_zone'] = 'right'
                if zone_repeat:
                    current_slide['_right_repeat'] = True
            elif zone_kind == 'LABEL':
                if current_slide.get('_split') and current_slide.get('_zone') == 'right':
                    if zone_value:
                        current = current_slide.get('_right_label') or ''
                        current_slide['_right_label'] = (
                            f'{current}\n{zone_value}' if current else zone_value
                        )
                elif zone_value:
                    _append_multiline(current_slide, 'title', zone_value)
            continue

        in_right_zone = bool(
            current_slide.get('_split') and current_slide.get('_zone') == 'right'
        )

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
            elif marker == 'VOICE':
                _append_multiline(current_slide, 'voice_script', value)
            elif marker in _VISUAL_MARKERS:
                _append_multiline(current_slide, 'visual_prompt', value)
            elif in_right_zone:
                if marker == 'KATEX':
                    for split_line in _split_katex_line_by_width(value, max_chars):
                        current_slide['_right_katex'].append(split_line)
                elif marker == 'TITLE':
                    current = current_slide.get('_right_label') or ''
                    current_slide['_right_label'] = (
                        f'{current}\n{value}' if current else value
                    )
                # TEXT/QUESTION inside RIGHT block: ignored (RIGHT is reference-only)
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
            continue

        if in_right_zone:
            for split_line in _split_katex_line_by_width(stripped, max_chars):
                current_slide['_right_katex'].append(split_line)
        elif current_slide['slide_type'] in {ReelSlide.TYPE_HOOK, ReelSlide.TYPE_CTA}:
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
        layout_notes = ''
        if slide.get('_method'):
            method_label = (slide.get('title') or '').strip()
            method_katex = (slide.get('katex') or '').strip()
            if method_label or method_katex:
                last_right_block = {
                    'label': method_label,
                    'katex': method_katex,
                }
            try:
                layout_notes = json.dumps(
                    {'method': {
                        'label': method_label,
                        'katex': method_katex,
                    }},
                    ensure_ascii=False,
                )
            except (TypeError, ValueError):
                layout_notes = ''
        elif slide.get('_split'):
            right_block = None
            collected_lines = [ln for ln in (slide.get('_right_katex') or []) if ln]
            collected_label = (slide.get('_right_label') or '').strip()
            wants_repeat = bool(slide.get('_right_repeat'))
            if not collected_lines and not collected_label:
                wants_repeat = True

            if wants_repeat and last_right_block:
                right_block = last_right_block
            elif collected_lines or collected_label:
                right_block = {
                    'label': collected_label,
                    'katex': '\n'.join(collected_lines),
                }
                last_right_block = right_block

            if right_block:
                try:
                    layout_notes = json.dumps(
                        {'split': {
                            'label': right_block.get('label', ''),
                            'right_katex': right_block.get('katex', ''),
                        }},
                        ensure_ascii=False,
                    )
                except (TypeError, ValueError):
                    layout_notes = ''

        payload = _build_slide_payload(
            slide_type=slide.get('slide_type'),
            title=slide.get('title', ''),
            screen_text=slide.get('screen_text', ''),
            katex=slide.get('katex', ''),
            voice_script=slide.get('voice_script', ''),
            layout_notes=layout_notes,
            visual_prompt=slide.get('visual_prompt', ''),
        )
        if (
            payload['screen_text']
            or payload['katex']
            or payload['voice_script']
            or payload['title']
            or payload['layout_notes']
        ):
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
            elif marker in _VISUAL_MARKERS and value:
                raw_text_lines.append(f'Visuel: {value}')
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
        slide_katex_lines = (
            [katex_lines[index]]
            if slide_type == ReelSlide.TYPE_RESULT and index < len(katex_lines)
            else cumulative_katex
        )
        slides_payload.append({
            'slide_type': slide_type,
            'title': slide_title,
            'screen_text': _template_screen_text_for_slide(slide_type, cumulative_text),
            'katex': _to_aligned_katex(slide_katex_lines),
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


def _project_is_carousel(project):
    return str(getattr(project, 'format_type', '') or '').strip().lower() == 'carousel'


def _prepare_carousel_slides(slides_payload):
    for payload in slides_payload:
        if payload.get('slide_type') in {ReelSlide.TYPE_CUMULATIVE_KATEX, ReelSlide.TYPE_RESULT}:
            payload['slide_type'] = ReelSlide.TYPE_KATEX
        payload['voice_script'] = ''
        payload['katex_inline_with_previous'] = False
        payload['katex_inline_offset_percent'] = 0
        payload['katex_inline_vertical_offset_em'] = 0
        payload['katex_cumulative_gap_em'] = 0.4
        payload['katex_reset_cumulative'] = False
        payload['katex_reset_keep_previous_line'] = True
        payload['katex_reveal_with_speech'] = False
        payload['katex_drop_previous_line'] = False
    return slides_payload


def _slide_layout_meta(slide_or_payload):
    raw_notes = ''
    if isinstance(slide_or_payload, dict):
        raw_notes = slide_or_payload.get('layout_notes', '')
    else:
        raw_notes = getattr(slide_or_payload, 'layout_notes', '')
    raw_notes = str(raw_notes or '').strip()
    if not raw_notes:
        return {}
    try:
        parsed = json.loads(raw_notes)
    except (TypeError, ValueError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _slide_visual_prompt(slide):
    return str(_slide_layout_meta(slide).get('visual_prompt') or '').strip()


def _normalize_carousel_image_png(image_bytes):
    try:
        with Image.open(BytesIO(image_bytes)) as source:
            image = ImageOps.exif_transpose(source).convert('RGB')
            image = ImageOps.fit(
                image,
                (1080, 1350),
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            output = BytesIO()
            image.save(output, format='PNG', optimize=True)
            return output.getvalue()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        raise GeminiAPIError('Image Gemini invalide ou illisible.') from exc


CAROUSEL_TYPE_STYLE_HINTS = {
    'marketing': {
        'label': 'Marketing / Conversion',
        'mood': 'premium editorial, ambiance studio creatif tech, magazine business',
        'scene_hook': (
            "Hero produit OptiTAB: mockup d'interface elegant sur ordinateur portable (cartes "
            "abstraites bleu/blanc, sans texte lisible), lumiere douce de studio, ambiance "
            "premium agence creative, espace negatif pour overlay typographique."
        ),
        'scene_cta': (
            "Mockup d'ecran OptiTAB ouvert sur smartphone et ordinateur, ambiance lumineuse, "
            "esprit pro editorial, beaucoup d'espace propre pour CTA."
        ),
        'scene_content': (
            "Composition editoriale premium type magazine business, motifs geometriques discrets "
            "bleu/blanc, fond creme ou bleu pale, espace propre pour overlay typographique."
        ),
    },
    'quiz': {
        'label': 'Quiz / QCM',
        'mood': 'ludique, energique, gamifie, accents colores doux mais dynamiques',
        'scene_hook': (
            "Composition ludique premium: grands points d'interrogation abstraits en 3D doux, "
            "formes geometriques flottantes bleu/blanc, ambiance jeu pedagogique haut de gamme, "
            "espace central libre pour overlay typographique."
        ),
        'scene_cta': (
            "Trophee abstrait stylise ou icone de validation en 3D soft, accents dores tres "
            "discrets, fond bleu lumineux, ambiance recompense ludique premium, espace pour CTA."
        ),
        'scene_content': (
            "Cartes flottantes type QCM (cartes vides sans texte), formes geometriques ludiques, "
            "fond clair, ambiance jeu pedagogique premium, espace propre pour question/reponse."
        ),
    },
    'tips': {
        'label': 'Conseils & Astuces',
        'mood': 'inspirant, lumineux, ambiance conseil bienveillant',
        'scene_hook': (
            "Ampoule stylisee en 3D soft moderne (sans cliche), accents bleu OptiTAB, halo lumineux "
            "discret, ambiance inspiration premium, espace central libre pour overlay."
        ),
        'scene_cta': (
            "Composition inspirante: carnet ouvert et stylo elegants stylises, lumiere douce, "
            "ambiance bureau premium, espace propre pour CTA."
        ),
        'scene_content': (
            "Post-it modernes stylises ou cartes de conseils abstraites (sans texte lisible), fond "
            "creme ou bleu pale, ambiance editoriale conseil, espace pour overlay typographique."
        ),
    },
    'avantapres': {
        'label': 'Avant / Apres',
        'mood': 'split-screen, transformation, contraste maitrise',
        'scene_hook': (
            "Composition split-screen subtile: cote gauche terne et brouillon (papier froisse "
            "abstrait, ambiance grise), cote droit lumineux et organise (interface OptiTAB "
            "abstraite bleu/blanc, sans texte), transition douce au centre, espace pour overlay."
        ),
        'scene_cta': (
            "Mockup d'eleve transforme: bureau propre, ordinateur ouvert sur interface OptiTAB "
            "abstraite, ambiance succes premium, lumiere chaude, espace pour CTA."
        ),
        'scene_content': (
            "Split-screen elegant avant/apres ou progression visuelle abstraite, contraste maitrise, "
            "fond clair, espace pour overlay typographique."
        ),
    },
    'story': {
        'label': 'Storytelling',
        'mood': 'narratif, cinematographique, ambiance recit premium',
        'scene_hook': (
            "Scene narrative cinematographique: silhouette d'eleve de dos face a un ordinateur "
            "stylise, lumiere de fenetre douce, ambiance recit premium, espace pour overlay."
        ),
        'scene_cta': (
            "Plan large cinematographique: bureau eclaire, ordinateur ouvert sur interface "
            "abstraite OptiTAB, ambiance fin de chapitre premium, espace pour CTA."
        ),
        'scene_content': (
            "Composition narrative editoriale: livre ouvert stylise, cahier, lumiere douce de "
            "fenetre, ambiance recit premium, espace propre pour texte."
        ),
    },
    'notion': {
        'label': 'Notion pedagogique',
        'mood': 'pedagogique premium, tableau noir moderne, formules abstraites',
        'scene_hook': (
            "Tableau noir moderne stylise avec formules mathematiques tres abstraites (sans "
            "texte ni symbole lisible), accents bleu OptiTAB, ambiance prof premium, espace "
            "central libre pour overlay typographique."
        ),
        'scene_cta': (
            "Bureau d'etudiant premium: cahier ouvert stylise, calculatrice moderne abstraite, "
            "lumiere douce, ambiance reussite scolaire, espace pour CTA."
        ),
        'scene_content': (
            "Tableau noir ou whiteboard premium avec formes mathematiques tres abstraites "
            "(courbes, formes geometriques, sans texte lisible), accents bleu OptiTAB, fond "
            "neutre, espace propre pour overlay typographique."
        ),
    },
}

DEFAULT_CAROUSEL_TYPE = 'marketing'


def _resolve_carousel_type(carousel_type):
    key = str(carousel_type or '').strip().lower()
    if key in CAROUSEL_TYPE_STYLE_HINTS:
        return key
    return DEFAULT_CAROUSEL_TYPE


def _build_carousel_slide_image_prompt(*, project, slide, total_slides, carousel_type=DEFAULT_CAROUSEL_TYPE):
    visual_prompt = _slide_visual_prompt(slide)
    slide_type = str(slide.slide_type or '').strip().lower()
    is_first = int(slide.order or 0) == 1
    is_last = bool(int(slide.order or 0) == int(total_slides or 0) and total_slides)

    style = CAROUSEL_TYPE_STYLE_HINTS.get(_resolve_carousel_type(carousel_type)) or CAROUSEL_TYPE_STYLE_HINTS[DEFAULT_CAROUSEL_TYPE]

    if slide_type == 'hook' or is_first:
        composition_hint = (
            "Composition centree facon affiche premium. Laisser une grande zone vide au centre et en bas "
            "pour qu'un overlay typographique soit ajoute ensuite par l'application."
        )
        scene_hint = style['scene_hook']
    elif slide_type == 'cta' or is_last:
        composition_hint = (
            "Composition finale invitante. Le sujet visuel occupe le haut ou un cote, et au moins 60% de l'image "
            "(centre + bas) reste un aplat doux pour overlay texte."
        )
        scene_hint = style['scene_cta']
    else:
        composition_hint = (
            "Composition asymetrique editoriale: sujet visuel sur un cote ou en haut, au moins 50% de l'image "
            "(idealement le bas et un cote) reste un aplat doux propre pour overlay texte."
        )
        scene_hint = style['scene_content']

    visual_block = visual_prompt or scene_hint
    mood_hint = style.get('mood') or ''

    return (
        "Generate an image. Output ONLY an image (no text response).\n\n"
        "TASK: Produce a clean background visual for an Instagram carousel slide for OptiTAB (optitab.net), "
        "a French math learning platform. The image will be used as a background, and a clean text overlay "
        "will be added later by the app.\n\n"
        f"SLIDE: {slide.order} of {total_slides} (type: {slide_type or 'content'})\n"
        f"PROJECT: {project.title or 'Carrousel OptiTAB'}\n"
        f"CAROUSEL STYLE: {style['label']} -- {mood_hint}\n\n"
        "VISUAL SUBJECT:\n"
        f"{visual_block}\n\n"
        "COMPOSITION:\n"
        f"{composition_hint}\n\n"
        "ART DIRECTION (must stay consistent across the carousel):\n"
        "- Aspect ratio 4:5 portrait (1080x1350 px).\n"
        "- Palette: OptiTAB deep blue (#29428e), soft blue, off-white, cool pastel accents.\n"
        "- Style: premium editorial education, clean, modern, bright, lots of soft blue/white space.\n"
        "- Render: clean 3D / vector / soft photo, sharp lines, gentle shadows.\n\n"
        "SCREEN MOCKUPS (when the scene contains an ordinateur / smartphone / tablette):\n"
        "- The screen content MUST faithfully replicate the OptiTAB interface visible in the "
        "REFERENCE IMAGES attached above (same colored cards, same blue header, same sidebar "
        "navigation, same dashboard / leaderboard / chapter cards layout, same OptiTAB logo "
        "placement, same typography style).\n"
        "- Text inside the mockup screens CAN be present and slightly readable to make it look "
        "like the real OptiTAB product (chapter names, XP, level, button labels). Keep it "
        "natural and short, do NOT invent fake brand text or unrelated copy.\n"
        "- The OptiTAB logo can appear inside the mockup screens, but nowhere else in the image.\n\n"
        "OUTSIDE the screen mockups (environment, background, surroundings):\n"
        "- NO readable text, words, headlines or fake quotes floating in the environment.\n"
        "- Keep large clean / soft areas (around 50%-60% of the image) free of busy detail so a "
        "typographic overlay can be added on top by the app.\n\n"
        "STRICT RULES:\n"
        "- No other brand logos (Apple, Google, etc.), no watermark, no signature.\n"
        "- No recognizable photoreal faces (prefer silhouettes, hands, back views, or illustrations).\n"
        "- No fake prices, no sensational claims, no clutter.\n\n"
        "OUTPUT: a single premium image where the device screens look like the real OptiTAB "
        "product (per the reference images) and the rest of the image leaves room for a "
        "typographic overlay added later by the app."
    )


SLIDE_IMAGE_STRATEGIES = {'hook_cta', 'hook', 'cta', 'all', 'none', 'custom'}
DEFAULT_SLIDE_IMAGE_STRATEGY = 'hook_cta'


def _is_hook_slide(slide):
    return str(slide.slide_type or '').strip().lower() == 'hook' or int(slide.order or 0) == 1


def _is_cta_slide(slide, total):
    if str(slide.slide_type or '').strip().lower() == 'cta':
        return True
    if total and int(slide.order or 0) == int(total):
        return True
    return False


def _filter_slides_for_image_generation(slides, strategy, slide_ids=None):
    strategy = (strategy or DEFAULT_SLIDE_IMAGE_STRATEGY).strip().lower()
    if strategy not in SLIDE_IMAGE_STRATEGIES:
        strategy = DEFAULT_SLIDE_IMAGE_STRATEGY
    if strategy == 'none':
        return []
    if strategy == 'all':
        return list(slides)
    if strategy == 'custom':
        try:
            ids = {int(sid) for sid in (slide_ids or [])}
        except (TypeError, ValueError):
            ids = set()
        return [s for s in slides if s.id in ids]

    total = len(slides)
    hook = next((s for s in slides if _is_hook_slide(s)), None)
    cta = next((s for s in reversed(slides) if _is_cta_slide(s, total)), None)
    if cta is hook:
        cta = None
    if strategy == 'hook':
        return [hook] if hook else []
    if strategy == 'cta':
        return [cta] if cta else []
    # hook_cta default
    result = []
    if hook:
        result.append(hook)
    if cta:
        result.append(cta)
    return result


def _generate_carousel_slide_images(*, project, user, strategy=DEFAULT_SLIDE_IMAGE_STRATEGY, slide_ids=None, carousel_type=DEFAULT_CAROUSEL_TYPE, use_site_references=True):
    slides = list(project.slides.order_by('order', 'id'))
    targets = _filter_slides_for_image_generation(slides, strategy, slide_ids=slide_ids)
    image_model_id = str(getattr(settings, 'GEMINI_IMAGE_MODEL_ID', 'gemini-2.5-flash-image') or 'gemini-2.5-flash-image').strip()
    generated = []
    errors = []
    resolved_type = _resolve_carousel_type(carousel_type)

    for slide in targets:
        prompt = _build_carousel_slide_image_prompt(
            project=project,
            slide=slide,
            total_slides=len(slides),
            carousel_type=resolved_type,
        )
        try:
            result = generate_carousel_image(
                prompt=prompt,
                model_id=image_model_id,
                aspect_ratio='3:4',
                return_metadata=True,
                use_site_references=use_site_references,
            )
            image_bytes = _normalize_carousel_image_png(result.get('image_bytes') or b'')
        except (GeminiConfigurationError, GeminiAPIError) as exc:
            errors.append({
                'slide_id': slide.id,
                'order': slide.order,
                'detail': str(exc),
            })
            continue

        filename = f'carousel_slide_{slide.order}_{uuid.uuid4().hex[:10]}.png'
        slide.generated_image.save(filename, ContentFile(image_bytes), save=False)
        slide.generated_image_prompt = prompt
        slide.generated_image_model_id = result.get('model_id') or image_model_id
        slide.generated_image_generated_at = timezone.now()
        slide.save(update_fields=[
            'generated_image',
            'generated_image_prompt',
            'generated_image_model_id',
            'generated_image_generated_at',
            'updated_at',
        ])
        usage_log = _record_gemini_usage(
            project=project,
            user=user,
            model_id=result.get('model_id') or image_model_id,
            prompt=prompt,
            generated_text='[image]',
            usage=result.get('usage') or {},
            cost=result.get('cost') or {},
            request_type='carousel_image_generation',
        )
        generated.append({
            'slide_id': slide.id,
            'order': slide.order,
            'usage_log_id': usage_log.id,
            'model_id': usage_log.model_id,
            'total_cost_usd': _decimal_to_float(usage_log.total_cost_usd),
            'display_cost': _decimal_to_float(_gemini_display_amount(usage_log.total_cost_usd)),
        })

    return {
        'generated': generated,
        'errors': errors,
        'strategy': strategy,
        'carousel_type': resolved_type,
        'targeted_count': len(targets),
        'total_slides': len(slides),
    }


def _decimal_to_float(value):
    if value is None:
        return 0.0
    return float(value)


def _current_month_start():
    now = timezone.now()
    return now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _gemini_display_amount(usd_value):
    currency = str(getattr(settings, 'GEMINI_DISPLAY_CURRENCY', 'USD') or 'USD').upper()
    amount = Decimal(str(usd_value or 0))
    if currency == 'EUR':
        amount *= Decimal(str(getattr(settings, 'GEMINI_EUR_PER_USD', 0.92) or 0.92))
    return amount


def _gemini_usage_summary():
    month_start = _current_month_start()
    queryset = GeminiUsageLog.objects.filter(created_at__gte=month_start)
    spent = queryset.aggregate(total=Sum('total_cost_usd')).get('total') or Decimal('0')
    display_currency = str(getattr(settings, 'GEMINI_DISPLAY_CURRENCY', 'USD') or 'USD').upper()
    if display_currency == 'EUR':
        display_spent = _gemini_display_amount(spent)
        display_budget = Decimal(str(getattr(settings, 'GEMINI_MONTHLY_BUDGET_EUR', 0) or 0))
    else:
        display_spent = spent
        display_budget = Decimal(str(getattr(settings, 'GEMINI_MONTHLY_BUDGET_USD', 0) or 0))
    display_remaining = max(display_budget - display_spent, Decimal('0')) if display_budget > 0 else None
    recent = []

    for item in queryset.select_related('reel_project', 'user')[:10]:
        display_item_cost = _gemini_display_amount(item.total_cost_usd)
        recent.append({
            'id': item.id,
            'created_at': item.created_at,
            'model_id': item.model_id,
            'project_id': item.reel_project_id,
            'project_title': item.reel_project.title if item.reel_project else '',
            'prompt_token_count': item.prompt_token_count,
            'candidates_token_count': item.candidates_token_count,
            'thoughts_token_count': item.thoughts_token_count,
            'total_token_count': item.total_token_count,
            'total_cost_usd': _decimal_to_float(item.total_cost_usd),
            'display_cost': _decimal_to_float(display_item_cost),
        })

    return {
        'month_start': month_start,
        'spent_usd': _decimal_to_float(spent),
        'budget_usd': _decimal_to_float(Decimal(str(getattr(settings, 'GEMINI_MONTHLY_BUDGET_USD', 0) or 0))) or None,
        'remaining_usd': None,
        'display_currency': display_currency,
        'display_spent': _decimal_to_float(display_spent),
        'display_budget': _decimal_to_float(display_budget) if display_budget > 0 else None,
        'display_remaining': _decimal_to_float(display_remaining) if display_remaining is not None else None,
        'eur_per_usd': _decimal_to_float(Decimal(str(getattr(settings, 'GEMINI_EUR_PER_USD', 0.92) or 0.92))),
        'usage_count': queryset.count(),
        'recent': recent,
    }


def _record_gemini_usage(*, project, user, model_id, prompt, generated_text, usage, cost, request_type='carousel_generation'):
    usage = usage or {}
    cost = cost or {}
    return GeminiUsageLog.objects.create(
        request_type=request_type,
        reel_project=project,
        user=user if getattr(user, 'is_authenticated', False) else None,
        model_id=model_id,
        prompt_token_count=usage.get('prompt_token_count') or 0,
        candidates_token_count=usage.get('candidates_token_count') or 0,
        thoughts_token_count=usage.get('thoughts_token_count') or 0,
        total_token_count=usage.get('total_token_count') or 0,
        input_cost_usd=cost.get('input_cost_usd') or Decimal('0'),
        output_cost_usd=cost.get('output_cost_usd') or Decimal('0'),
        total_cost_usd=cost.get('total_cost_usd') or Decimal('0'),
        pricing_source=cost.get('pricing_source') or '',
        prompt_chars=len(str(prompt or '')),
        response_chars=len(str(generated_text or '')),
    )


def _replace_project_slides(project, slides_payload, instagram_caption=''):
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
                    katex_inline_with_previous=payload.get('katex_inline_with_previous', False),
                    katex_inline_offset_percent=payload.get('katex_inline_offset_percent', 0),
                    katex_inline_vertical_offset_em=payload.get('katex_inline_vertical_offset_em', 0),
                    katex_cumulative_gap_em=payload.get('katex_cumulative_gap_em', 0.4),
                    katex_reset_cumulative=payload.get('katex_reset_cumulative', False),
                    katex_reset_keep_previous_line=payload.get('katex_reset_keep_previous_line', True),
                    katex_reveal_with_speech=payload.get('katex_reveal_with_speech', False),
                    katex_drop_previous_line=payload.get('katex_drop_previous_line', False),
                    duration_seconds=payload.get('duration_seconds', 4),
                    layout_status=ReelSlide.LAYOUT_UNCHECKED,
                    layout_notes=payload.get('layout_notes', ''),
                )
            )

        ReelSlide.objects.bulk_create(slides_to_create)

        project.slide_count = len(slides_to_create)
        project.status = ReelProject.STATUS_DRAFT
        project.instagram_caption = instagram_caption
        project.save(update_fields=['slide_count', 'status', 'instagram_caption', 'updated_at'])

    return ReelProject.objects.prefetch_related('slides').get(pk=project.pk)


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


class ReelGeminiOptionsView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request):
        return Response({
            'models': list_gemini_models(),
            'default_model_id': getattr(settings, 'GEMINI_MODEL_ID', 'gemini-2.5-flash') or 'gemini-2.5-flash',
            'usage': _gemini_usage_summary(),
        })


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
        if _project_is_carousel(project):
            slides_payload = _prepare_carousel_slides(slides_payload)
        if not slides_payload:
            return Response(
                {'detail': "Aucune ligne exploitable trouvée dans le template."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = _replace_project_slides(project, slides_payload, instagram_caption)
        return Response(_project_serializer(project, request, detail=True).data, status=status.HTTP_201_CREATED)


class ReelProjectGenerateCarouselWithGeminiView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        if not _project_is_carousel(project):
            return Response(
                {'detail': 'La génération Gemini est disponible uniquement pour les carrousels.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ReelGeminiCarouselGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            gemini_result = generate_carousel_template(
                prompt=serializer.validated_data['prompt'],
                model_id=serializer.validated_data.get('model_id', ''),
                return_metadata=True,
            )
        except GeminiConfigurationError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except GeminiAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        if isinstance(gemini_result, dict):
            generated_template_text = gemini_result.get('text', '')
            resolved_model_id = gemini_result.get('model_id') or serializer.validated_data.get('model_id', '')
            usage = gemini_result.get('usage') or {}
            cost = gemini_result.get('cost') or {}
        else:
            generated_template_text = str(gemini_result or '')
            resolved_model_id = serializer.validated_data.get('model_id', '') or getattr(settings, 'GEMINI_MODEL_ID', 'gemini-2.5-flash')
            usage = {}
            cost = {}

        clean_template_text, instagram_caption = _extract_instagram_caption(generated_template_text)
        template_payload = {
            'template_text': clean_template_text,
            'max_chars_per_line': serializer.validated_data.get('max_chars_per_line', 38),
        }
        slides_payload = _prepare_carousel_slides(_build_template_slides(project, template_payload))
        if not slides_payload:
            return Response(
                {
                    'detail': 'Gemini a repondu, mais aucune slide exploitable n a ete trouvee.',
                    'template_text': generated_template_text,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        project = _replace_project_slides(project, slides_payload, instagram_caption)
        usage_log = _record_gemini_usage(
            project=project,
            user=request.user,
            model_id=resolved_model_id,
            prompt=serializer.validated_data['prompt'],
            generated_text=generated_template_text,
            usage=usage,
            cost=cost,
        )
        image_generation = {'generated': [], 'errors': []}
        if serializer.validated_data.get('generate_images', True):
            image_generation = _generate_carousel_slide_images(
                project=project,
                user=request.user,
                strategy=serializer.validated_data.get('slide_image_strategy') or DEFAULT_SLIDE_IMAGE_STRATEGY,
                slide_ids=serializer.validated_data.get('slide_image_ids') or None,
                carousel_type=serializer.validated_data.get('carousel_type') or DEFAULT_CAROUSEL_TYPE,
                use_site_references=bool(serializer.validated_data.get('use_site_references', True)),
            )
            project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)

        return Response(
            {
                'project': _project_serializer(project, request, detail=True).data,
                'template_text': generated_template_text,
                'image_generation': image_generation,
                'gemini_usage': {
                    'id': usage_log.id,
                    'model_id': usage_log.model_id,
                    'prompt_token_count': usage_log.prompt_token_count,
                    'candidates_token_count': usage_log.candidates_token_count,
                    'thoughts_token_count': usage_log.thoughts_token_count,
                    'total_token_count': usage_log.total_token_count,
                    'input_cost_usd': _decimal_to_float(usage_log.input_cost_usd),
                    'output_cost_usd': _decimal_to_float(usage_log.output_cost_usd),
                    'total_cost_usd': _decimal_to_float(usage_log.total_cost_usd),
                    'display_cost': _decimal_to_float(_gemini_display_amount(usage_log.total_cost_usd)),
                },
                'gemini_summary': _gemini_usage_summary(),
            },
            status=status.HTTP_201_CREATED,
        )


class ReelProjectRegenerateCarouselImagesView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject.objects.prefetch_related('slides'), pk=pk)
        if not _project_is_carousel(project):
            return Response(
                {'detail': 'La régénération d images Gemini est disponible uniquement pour les carrousels.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not project.slides.exists():
            return Response(
                {'detail': 'Ce carrousel n a pas encore de slides. Génère d abord le texte.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        body = request.data if isinstance(request.data, dict) else {}
        strategy = str(body.get('slide_image_strategy') or DEFAULT_SLIDE_IMAGE_STRATEGY).strip().lower()
        if strategy not in SLIDE_IMAGE_STRATEGIES:
            strategy = DEFAULT_SLIDE_IMAGE_STRATEGY
        carousel_type = _resolve_carousel_type(body.get('carousel_type'))
        slide_ids = body.get('slide_image_ids') if strategy == 'custom' else None
        use_site_references = body.get('use_site_references')
        use_site_references = True if use_site_references is None else bool(use_site_references)

        image_generation = _generate_carousel_slide_images(
            project=project,
            user=request.user,
            strategy=strategy,
            slide_ids=slide_ids,
            carousel_type=carousel_type,
            use_site_references=use_site_references,
        )
        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(
            {
                'project': _project_serializer(project, request, detail=True).data,
                'image_generation': image_generation,
                'gemini_summary': _gemini_usage_summary(),
            },
            status=status.HTTP_200_OK,
        )


class ReelSlideGenerateImageView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        slide = get_object_or_404(ReelSlide.objects.select_related('reel_project'), pk=pk)
        project = slide.reel_project
        if not _project_is_carousel(project):
            return Response(
                {'detail': "La génération d'image est disponible uniquement pour les carrousels."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        body = request.data if isinstance(request.data, dict) else {}
        custom_prompt = str(body.get('prompt') or '').strip()
        carousel_type = _resolve_carousel_type(body.get('carousel_type'))
        model_id = str(body.get('model_id') or getattr(settings, 'GEMINI_IMAGE_MODEL_ID', 'gemini-2.5-flash-image') or '').strip()
        use_site_references_raw = body.get('use_site_references')
        use_site_references = True if use_site_references_raw is None else bool(use_site_references_raw)

        total_slides = project.slides.count()
        if custom_prompt:
            prompt = custom_prompt
        else:
            prompt = _build_carousel_slide_image_prompt(
                project=project,
                slide=slide,
                total_slides=total_slides,
                carousel_type=carousel_type,
            )

        try:
            result = generate_carousel_image(
                prompt=prompt,
                model_id=model_id,
                aspect_ratio='3:4',
                return_metadata=True,
                use_site_references=use_site_references,
            )
            image_bytes = _normalize_carousel_image_png(result.get('image_bytes') or b'')
        except (GeminiConfigurationError, GeminiAPIError) as exc:
            return Response(
                {'detail': str(exc)},
                status=status.HTTP_502_BAD_GATEWAY,
            )

        filename = f'carousel_slide_{slide.order}_{uuid.uuid4().hex[:10]}.png'
        slide.generated_image.save(filename, ContentFile(image_bytes), save=False)
        slide.generated_image_prompt = prompt
        slide.generated_image_model_id = result.get('model_id') or model_id
        slide.generated_image_generated_at = timezone.now()
        slide.save(update_fields=[
            'generated_image',
            'generated_image_prompt',
            'generated_image_model_id',
            'generated_image_generated_at',
            'updated_at',
        ])

        usage_log = _record_gemini_usage(
            project=project,
            user=request.user,
            model_id=result.get('model_id') or model_id,
            prompt=prompt,
            generated_text='[image]',
            usage=result.get('usage') or {},
            cost=result.get('cost') or {},
            request_type='carousel_image_generation',
        )

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(
            {
                'project': _project_serializer(project, request, detail=True).data,
                'slide_id': slide.id,
                'prompt': prompt,
                'used_custom_prompt': bool(custom_prompt),
                'model_id': usage_log.model_id,
                'gemini_summary': _gemini_usage_summary(),
            },
            status=status.HTTP_200_OK,
        )


class ReelSlideClearImageView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        slide = get_object_or_404(ReelSlide.objects.select_related('reel_project'), pk=pk)
        project = slide.reel_project
        if not _project_is_carousel(project):
            return Response(
                {'detail': "Cette action est disponible uniquement pour les carrousels."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if slide.generated_image:
            slide.generated_image.delete(save=False)
        slide.generated_image = None
        slide.generated_image_prompt = ''
        slide.generated_image_model_id = ''
        slide.generated_image_generated_at = None
        slide.save(update_fields=[
            'generated_image',
            'generated_image_prompt',
            'generated_image_model_id',
            'generated_image_generated_at',
            'updated_at',
        ])

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(
            {
                'project': _project_serializer(project, request, detail=True).data,
                'slide_id': slide.id,
            },
            status=status.HTTP_200_OK,
        )


class ReelImageInstructionsView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request):
        return Response(
            {
                'instructions': read_image_instructions(),
                'max_length': IMAGE_INSTRUCTIONS_MAX_LENGTH,
            },
            status=status.HTTP_200_OK,
        )

    def put(self, request):
        body = request.data if isinstance(request.data, dict) else {}
        text = str(body.get('instructions') or '')
        saved = write_image_instructions(text)
        return Response(
            {
                'instructions': saved,
                'max_length': IMAGE_INSTRUCTIONS_MAX_LENGTH,
            },
            status=status.HTTP_200_OK,
        )


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
                katex_inline_with_previous=payload.get('katex_inline_with_previous', False),
                katex_inline_offset_percent=payload.get('katex_inline_offset_percent', 0),
                katex_inline_vertical_offset_em=payload.get('katex_inline_vertical_offset_em', 0),
                katex_cumulative_gap_em=payload.get('katex_cumulative_gap_em', 0.4),
                katex_reset_cumulative=payload.get('katex_reset_cumulative', False),
                katex_reset_keep_previous_line=payload.get('katex_reset_keep_previous_line', True),
                katex_reveal_with_speech=payload.get('katex_reveal_with_speech', False),
                katex_drop_previous_line=payload.get('katex_drop_previous_line', False),
                duration_seconds=payload.get('duration_seconds', DEFAULT_TEMPLATE_SLIDE_DURATION_SECONDS),
                layout_status=ReelSlide.LAYOUT_UNCHECKED,
                layout_notes=payload.get('layout_notes', ''),
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
        for field_name in (
            'katex_inline_with_previous',
            'katex_inline_offset_percent',
            'katex_inline_vertical_offset_em',
            'katex_cumulative_gap_em',
            'katex_reset_cumulative',
            'katex_reset_keep_previous_line',
            'katex_reveal_with_speech',
            'katex_drop_previous_line',
        ):
            if field_name in payload:
                field_values[field_name] = payload[field_name]

        for field_name, field_value in field_values.items():
            if getattr(slide, field_name) != field_value:
                setattr(slide, field_name, field_value)
                update_fields.append(field_name)

        content_changed = any(
            field_name in update_fields
            for field_name in ('slide_type', 'title', 'screen_text', 'katex', 'voice_script', 'duration_seconds')
        )
        new_layout_notes = payload.get('layout_notes', '') or ''
        if content_changed:
            slide.layout_status = ReelSlide.LAYOUT_UNCHECKED
            update_fields.append('layout_status')
        if (slide.layout_notes or '') != new_layout_notes:
            slide.layout_notes = new_layout_notes
            update_fields.append('layout_notes')

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
        if _project_is_carousel(project):
            slides_payload = _prepare_carousel_slides(slides_payload)
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

        if _project_is_carousel(project):
            return Response(
                {'detail': 'Les carrousels OptiTAB sont exportes en images: aucune voix a generer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        tts_text = _apply_pronunciation_overrides(
            speech_text,
            project.pronunciation_overrides or [],
        )

        try:
            tts_result = tts_generate_speech(
                text=tts_text,
                **_speech_generation_kwargs(serializer.validated_data),
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


class ReelVoiceLibraryView(APIView):
    """Return ElevenLabs Voice Library choices for exploration in the admin UI."""
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request):
        language = str(request.query_params.get('language') or 'fr').strip().lower()
        accent = str(request.query_params.get('accent') or 'parisian').strip().lower()
        category = str(request.query_params.get('category') or '').strip().lower()
        gender = str(request.query_params.get('gender') or '').strip().lower()
        age = str(request.query_params.get('age') or '').strip().lower()
        search = str(request.query_params.get('search') or '').strip()
        featured = request.query_params.get('featured')
        page_size = request.query_params.get('page_size') or 60
        page = request.query_params.get('page') or 0

        try:
            payload = list_shared_voices(
                language=language,
                accent=accent,
                category=category,
                gender=gender,
                age=age,
                search=search,
                featured=featured,
                page_size=page_size,
                page=page,
            )
        except ElevenLabsConfigurationError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except ElevenLabsAPIError as exc:
            return Response({'detail': str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

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
                **_speech_generation_kwargs(serializer.validated_data),
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

        if _project_is_carousel(project):
            return Response(
                {'detail': 'Les carrousels OptiTAB sont exportes en images: aucune voix a generer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
                    **_speech_generation_kwargs(serializer.validated_data),
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
                show_subtitles=serializer.validated_data.get('show_subtitles', False),
                subtitle_offset_percent=serializer.validated_data.get('subtitle_offset_percent'),
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

        if _project_is_carousel(slide.reel_project):
            return Response(
                {'detail': 'Les carrousels OptiTAB sont exportes en images: aucune voix a generer.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        requested_text = str(serializer.validated_data.get('text') or '').strip()
        speech_text = requested_text or build_slide_speech_text(slide)

        try:
            slide = _generate_and_save_slide_speech(
                slide,
                speech_text=speech_text,
                **_speech_generation_kwargs(serializer.validated_data),
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
        if _project_is_carousel(slide.reel_project):
            next_slide_type = serializer.validated_data.get('slide_type', slide.slide_type)
            if next_slide_type in {ReelSlide.TYPE_CUMULATIVE_KATEX, ReelSlide.TYPE_RESULT}:
                serializer.validated_data['slide_type'] = ReelSlide.TYPE_KATEX
            serializer.validated_data['voice_script'] = ''
            serializer.validated_data['katex_inline_with_previous'] = False
            serializer.validated_data['katex_inline_offset_percent'] = 0
            serializer.validated_data['katex_inline_vertical_offset_em'] = 0
            serializer.validated_data['katex_cumulative_gap_em'] = 0.4
            serializer.validated_data['katex_reset_cumulative'] = False
            serializer.validated_data['katex_reset_keep_previous_line'] = True
            serializer.validated_data['katex_reveal_with_speech'] = False
            serializer.validated_data['katex_drop_previous_line'] = False
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
