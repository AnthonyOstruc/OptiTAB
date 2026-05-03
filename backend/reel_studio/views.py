import re

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
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
    ReelTemplateGenerateSerializer,
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
    template_text = payload['template_text']
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
        serializer = ReelProjectSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReelProjectSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = serializer.save()
        detail_serializer = ReelProjectDetailSerializer(project)
        return Response(detail_serializer.data, status=status.HTTP_201_CREATED)


class ReelProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def get(self, request, pk):
        project = get_object_or_404(ReelProject.objects.prefetch_related('slides'), pk=pk)
        serializer = ReelProjectDetailSerializer(project)
        return Response(serializer.data)

    def patch(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        serializer = ReelProjectSerializer(project, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_project = serializer.save()
        detail_serializer = ReelProjectDetailSerializer(updated_project)
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
            project.save(update_fields=['slide_count', 'status', 'updated_at'])

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        serializer = ReelProjectDetailSerializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReelProjectGenerateFromTemplateView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def post(self, request, pk):
        project = get_object_or_404(ReelProject, pk=pk)
        serializer = ReelTemplateGenerateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        slides_payload = _build_template_slides(project, serializer.validated_data)
        if not slides_payload:
            return Response(
                {'detail': "Aucune ligne exploitable trouvée dans le template."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
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
            project.save(update_fields=['slide_count', 'status', 'updated_at'])

        project = ReelProject.objects.prefetch_related('slides').get(pk=project.pk)
        return Response(ReelProjectDetailSerializer(project).data, status=status.HTTP_201_CREATED)


class ReelSlideDetailView(APIView):
    permission_classes = [IsAuthenticated, IsStaffOrSuperuser]

    def patch(self, request, pk):
        slide = get_object_or_404(ReelSlide, pk=pk)
        serializer = ReelSlideSerializer(slide, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_slide = serializer.save()
        _touch_project(updated_slide.reel_project_id)
        return Response(ReelSlideSerializer(updated_slide).data)

    def delete(self, request, pk):
        slide = get_object_or_404(ReelSlide, pk=pk)
        project_id = slide.reel_project_id
        slide.delete()

        slide_count = ReelSlide.objects.filter(reel_project_id=project_id).count()
        ReelProject.objects.filter(pk=project_id).update(
            slide_count=slide_count,
            updated_at=timezone.now(),
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
