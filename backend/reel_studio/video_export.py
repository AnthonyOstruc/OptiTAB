import base64
import binascii
import os
import re
import shutil
import subprocess
import tempfile
from io import BytesIO

from django.conf import settings
from PIL import Image, ImageOps, UnidentifiedImageError


class VideoExportConfigurationError(Exception):
    pass


class VideoExportError(Exception):
    pass


MAX_FRAME_BYTES = 20 * 1024 * 1024
DEFAULT_AUDIO_BITRATE = '192k'
DEFAULT_VIDEO_PRESET = 'veryfast'
DEFAULT_AUDIO_TAIL_PADDING_SECONDS = 0.25
DEFAULT_MAX_SEGMENT_SECONDS = 180.0


def _get_ffmpeg_executable():
    try:
        import imageio_ffmpeg

        executable = imageio_ffmpeg.get_ffmpeg_exe()
        if executable and os.path.exists(executable):
            return executable
    except Exception:
        pass

    executable = shutil.which('ffmpeg')
    if executable:
        return executable

    raise VideoExportConfigurationError(
        'FFmpeg indisponible. Installe les dependances backend avec requirements.txt.'
    )


def _run_ffmpeg(command, *, timeout):
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        raise VideoExportError('Timeout FFmpeg pendant l export video.') from exc

    if completed.returncode != 0:
        stderr = re.sub(r'\s+', ' ', completed.stderr or '').strip()
        detail = stderr[-1200:] if stderr else 'Erreur FFmpeg inconnue.'
        raise VideoExportError(detail)


def _get_ffprobe_executable(ffmpeg):
    ffmpeg_dir = os.path.dirname(os.path.abspath(ffmpeg))
    ffprobe_name = 'ffprobe.exe' if os.name == 'nt' else 'ffprobe'
    bundled = os.path.join(ffmpeg_dir, ffprobe_name)
    if os.path.exists(bundled):
        return bundled

    executable = shutil.which('ffprobe')
    if executable:
        return executable

    return ''


def _decode_frame_image(image_data):
    raw_value = str(image_data or '').strip()
    if not raw_value:
        raise VideoExportError('Image de slide manquante.')

    if ',' in raw_value and raw_value.lower().startswith('data:image/'):
        raw_value = raw_value.split(',', 1)[1]

    compact = re.sub(r'\s+', '', raw_value)
    try:
        image_bytes = base64.b64decode(compact, validate=True)
    except (binascii.Error, ValueError) as exc:
        raise VideoExportError('Image de slide invalide.') from exc

    if not image_bytes:
        raise VideoExportError('Image de slide vide.')
    if len(image_bytes) > MAX_FRAME_BYTES:
        raise VideoExportError('Image de slide trop lourde.')

    return image_bytes


def _save_frame_png(image_data, output_path, *, width, height):
    image_bytes = _decode_frame_image(image_data)
    try:
        with Image.open(BytesIO(image_bytes)) as source:
            image = ImageOps.exif_transpose(source).convert('RGB')
    except UnidentifiedImageError as exc:
        raise VideoExportError('Image de slide illisible.') from exc

    if image.size != (width, height):
        image = ImageOps.contain(image, (width, height), Image.Resampling.LANCZOS)
        canvas = Image.new('RGB', (width, height), (248, 251, 255))
        x = (width - image.width) // 2
        y = (height - image.height) // 2
        canvas.paste(image, (x, y))
        image = canvas

    image.save(output_path, 'PNG', optimize=True)


def _copy_audio_file(file_field, output_path):
    if not file_field:
        return False

    try:
        with file_field.open('rb') as source, open(output_path, 'wb') as target:
            shutil.copyfileobj(source, target)
    except Exception as exc:
        raise VideoExportError('Impossible de lire le MP3 de slide.') from exc

    return os.path.getsize(output_path) > 0


def _safe_duration(value):
    try:
        duration = float(value)
    except (TypeError, ValueError):
        duration = 4.0
    return min(30.0, max(1.0, duration))


def _max_segment_duration():
    try:
        configured = float(getattr(settings, 'REEL_VIDEO_MAX_SEGMENT_SECONDS', DEFAULT_MAX_SEGMENT_SECONDS) or DEFAULT_MAX_SEGMENT_SECONDS)
    except (TypeError, ValueError):
        configured = DEFAULT_MAX_SEGMENT_SECONDS
    return max(30.0, configured)


def _audio_tail_padding():
    try:
        configured = float(getattr(settings, 'REEL_VIDEO_AUDIO_TAIL_PADDING_SECONDS', DEFAULT_AUDIO_TAIL_PADDING_SECONDS) or DEFAULT_AUDIO_TAIL_PADDING_SECONDS)
    except (TypeError, ValueError):
        configured = DEFAULT_AUDIO_TAIL_PADDING_SECONDS
    return min(2.0, max(0.0, configured))


def _probe_audio_duration(audio_path, *, ffmpeg, timeout):
    ffprobe = _get_ffprobe_executable(ffmpeg)
    if ffprobe:
        command = [
            ffprobe,
            '-v',
            'error',
            '-show_entries',
            'format=duration',
            '-of',
            'default=noprint_wrappers=1:nokey=1',
            audio_path,
        ]
        try:
            completed = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=min(timeout, 60),
            )
            if completed.returncode == 0:
                duration = float((completed.stdout or '').strip())
                if duration > 0:
                    return duration
        except (subprocess.TimeoutExpired, TypeError, ValueError):
            pass

    command = [ffmpeg, '-hide_banner', '-i', audio_path, '-f', 'null', '-']
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=min(timeout, 120),
        )
    except subprocess.TimeoutExpired as exc:
        raise VideoExportError('Timeout FFmpeg pendant la lecture de duree audio.') from exc

    match = re.search(r'Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)', completed.stderr or '')
    if not match:
        raise VideoExportError('Impossible de lire la duree du MP3 de slide.')

    hours, minutes, seconds = match.groups()
    duration = (int(hours) * 3600) + (int(minutes) * 60) + float(seconds)
    if duration <= 0:
        raise VideoExportError('Duree MP3 de slide invalide.')
    return duration


def _segment_duration(*, requested_duration, audio_path, ffmpeg, timeout):
    if not audio_path:
        return _safe_duration(requested_duration)

    audio_duration = _probe_audio_duration(audio_path, ffmpeg=ffmpeg, timeout=timeout)
    duration = max(1.0, audio_duration + _audio_tail_padding())
    max_duration = _max_segment_duration()
    if duration > max_duration:
        raise VideoExportError(
            f'Audio de slide trop long pour l export video ({duration:.1f}s/{max_duration:.0f}s).'
        )
    return duration


def _video_filter(width, height):
    return (
        f'scale={width}:{height}:force_original_aspect_ratio=decrease,'
        f'pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1'
    )


def _ass_timestamp(seconds):
    seconds = max(0.0, float(seconds or 0))
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int(round((seconds - int(seconds)) * 100))
    if cs >= 100:
        cs = 99
    return f'{h:01d}:{m:02d}:{s:02d}.{cs:02d}'


_ASS_CONTROL_TAG_RE = re.compile(r'\[[^\]\r\n]*[A-Za-zÀ-ÖØ-öø-ÿ][^\]\r\n]*\]')


def _ass_clean_text(value):
    cleaned = _ASS_CONTROL_TAG_RE.sub(' ', str(value or ''))
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned


def _build_ass_subtitles_for_slide(slide, *, width, height, segment_duration, max_chars=30, subtitle_offset_percent=None):
    raw_timings = getattr(slide, 'speech_word_timings', None)
    if not isinstance(raw_timings, dict):
        return ''
    raw_words = raw_timings.get('words')
    if not isinstance(raw_words, list) or not raw_words:
        return ''

    parsed = []
    for entry in raw_words:
        if not isinstance(entry, dict):
            continue
        text = _ass_clean_text(entry.get('text'))
        if not text:
            continue
        try:
            start = float(entry.get('start'))
            end = float(entry.get('end'))
        except (TypeError, ValueError):
            continue
        if not (start >= 0 and end >= start):
            continue
        parsed.append({'text': text, 'start': start, 'end': end})

    if not parsed:
        return ''

    lines = []
    current = []
    chars = 0
    for word in parsed:
        sep = 1 if current else 0
        if current and chars + sep + len(word['text']) > max_chars:
            lines.append(current)
            current = [word]
            chars = len(word['text'])
        else:
            current.append(word)
            chars += sep + len(word['text'])
    if current:
        lines.append(current)
    if not lines:
        return ''

    # Detect vertical (Reel/TikTok 9:16) vs horizontal (YouTube 16:9) format.
    is_vertical = height > width

    # Font size: 3.8% of video width — matches preview's 3.8cqw
    font_size = max(28, int(round(width * 0.038)))
    margin_h = max(40, int(round(width * 0.04)))

    # Subtitle vertical position: % distance from the bottom edge of the frame.
    # Caller can override; defaults differ per orientation:
    #   • vertical (Reel/TikTok): 20% — well above the platform UI overlay.
    #   • horizontal (YouTube):    5% — close to bottom (no UI overlay).
    if subtitle_offset_percent is None:
        subtitle_offset_percent = 20.0 if is_vertical else 5.0
    subtitle_offset_percent = max(0.0, min(50.0, float(subtitle_offset_percent)))
    margin_v = max(int(round(height * subtitle_offset_percent / 100)), 30)

    # ASS colour format: &HAABBGGRR  (AA: 00=fully opaque, FF=fully transparent)
    primary_white = '&H00FFFFFF'   # bright white — past / spoken words
    secondary_white = '&H47FFFFFF'  # 72% opaque white — future / unspoken words
    active_blue = '&H00EB6325'      # #2563eb in BGR — active word highlight
    outline_black = '&H00000000'    # opaque black outline for legibility

    header = [
        '[Script Info]',
        'ScriptType: v4.00+',
        f'PlayResX: {int(width)}',
        f'PlayResY: {int(height)}',
        'WrapStyle: 0',
        'ScaledBorderAndShadow: yes',
        'YCbCr Matrix: TV.709',
        '',
        '[V4+ Styles]',
        ('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, '
         'OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, '
         'ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, '
         'Alignment, MarginL, MarginR, MarginV, Encoding'),
        # No background — strong black outline (4px) + drop shadow keep the
        # text readable on any slide content. BorderStyle 1 = outline + shadow.
        (f'Style: Default,Arial,{font_size},{primary_white},{secondary_white},'
         f'{outline_black},&H00000000,1,0,0,0,100,100,0,0,1,4,2,2,'
         f'{margin_h},{margin_h},{margin_v},1'),
        '',
        '[Events]',
        'Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text',
    ]

    events = []
    last_end = max(0.0, float(segment_duration or 0))

    for i, line_words in enumerate(lines):
        line_start = line_words[0]['start']
        if i + 1 < len(lines):
            line_end = lines[i + 1][0]['start']
        else:
            line_end = max(line_words[-1]['end'] + 0.4, last_end)
        if last_end > 0:
            line_end = min(line_end, last_end)
        if line_end <= line_start:
            line_end = line_start + 0.2

        # Per-state events: one Dialogue per word's active interval.
        # In each event the whole line is rendered with per-word colour overrides:
        #   • past words (already spoken)   → bright white (`primary_white`)
        #   • active word (currently spoken)→ white text with thick blue outline = blue highlight
        #   • future words (not yet spoken) → 72% opaque white (`secondary_white`)
        for j, active_word in enumerate(line_words):
            interval_start = active_word['start']
            if j + 1 < len(line_words):
                interval_end = line_words[j + 1]['start']
            else:
                interval_end = line_end
            interval_end = min(interval_end, line_end)
            if interval_end <= interval_start:
                continue

            text_parts = []
            for k, word in enumerate(line_words):
                word_text = word['text'].replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
                # IMPORTANT: ASS override tags PERSIST until re-set within a dialogue,
                # so we MUST explicitly write \bord and \3c on every word — otherwise
                # future words inherit the active word's thick blue outline.
                if k < j:
                    # Past — bright white, default 4px black outline
                    overrides = f'\\1c{primary_white}\\bord4\\3c{outline_black}'
                elif k == j:
                    # Active — white text with thick BLUE outline halo
                    overrides = f'\\1c{primary_white}\\bord10\\3c{active_blue}'
                else:
                    # Future — dim white, reset back to default 4px black outline
                    overrides = f'\\1c{secondary_white}\\bord4\\3c{outline_black}'

                tag = f'{{{overrides}}}'
                if k == 0:
                    text_parts.append(f'{tag}{word_text}')
                else:
                    text_parts.append(f' {tag}{word_text}')

            text = ''.join(text_parts)
            events.append(
                f'Dialogue: 0,{_ass_timestamp(interval_start)},{_ass_timestamp(interval_end)},'
                f'Default,,0,0,0,,{text}'
            )

    return '\n'.join(header + events) + '\n'


def _ffmpeg_subtitles_path(path):
    # Escape for ffmpeg's subtitles filter (which uses libass)
    escaped = path.replace('\\', '/').replace(':', '\\:').replace("'", "\\'")
    return escaped


def _create_subtitle_gradient_png(output_path, *, width, bar_height):
    """Render the subtitle gradient bar to a PNG (RGBA) for ffmpeg overlay.

    Reproduces the preview's CSS gradient pixel-perfectly:
      `linear-gradient(to top, rgba(15,40,100,0.88) 0%, rgba(15,40,100,0.5) 45%, transparent 100%)`

    A real per-pixel alpha gradient avoids the visible "stair-step" banding
    that stacking ASS rectangles produces.
    """
    if width <= 0 or bar_height <= 0:
        return

    R, G, B = 15, 40, 100

    # Build a single-pixel-wide column with the gradient, then resize horizontally.
    # NEAREST keeps each row's alpha intact.
    column = Image.new('RGBA', (1, bar_height), (R, G, B, 0))
    denom = max(1, bar_height - 1)
    for y in range(bar_height):
        # Position from the BOTTOM of the bar (0 = bottom, 1 = top of bar)
        pos_from_bottom = 1 - (y / denom)
        if pos_from_bottom <= 0.45:
            # Stop range [0%, 45%] from bottom: alpha 0.88 → 0.5
            t = pos_from_bottom / 0.45
            alpha = 0.88 + (0.5 - 0.88) * t
        else:
            # Stop range [45%, 100%] from bottom: alpha 0.5 → 0
            t = (pos_from_bottom - 0.45) / 0.55
            alpha = 0.5 * (1 - t)
        a = max(0, min(255, int(round(alpha * 255))))
        column.putpixel((0, y), (R, G, B, a))

    img = column.resize((width, bar_height), Image.NEAREST)
    img.save(output_path, 'PNG')


def _build_segment(
    *,
    ffmpeg,
    image_path,
    audio_path,
    output_path,
    duration,
    width,
    height,
    fps,
    crf,
    preset,
    timeout,
    subtitle_path='',
):
    duration_text = f'{duration:.3f}'
    base_vf = _video_filter(width, height)
    has_subtitles = bool(subtitle_path)

    # Inputs: [0]=image, [audio_idx]=audio (real file or silent anullsrc)
    inputs = [
        '-loop', '1', '-framerate', str(fps), '-t', duration_text, '-i', image_path,
    ]
    audio_idx = 1

    has_audio = bool(audio_path)
    if has_audio:
        inputs.extend(['-i', audio_path])
    else:
        inputs.extend([
            '-f', 'lavfi', '-t', duration_text,
            '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100',
        ])

    # Single -vf chain: scale to target resolution, then burn ASS subtitles if any.
    vf = f"{base_vf},subtitles='{_ffmpeg_subtitles_path(subtitle_path)}'" if has_subtitles else base_vf
    video_args = [
        '-vf', vf,
        '-map', '0:v:0',
        '-map', f'{audio_idx}:a:0',
    ]

    common_video = [
        '-r', str(fps),
        '-c:v', 'libx264',
        '-preset', preset,
        '-crf', str(crf),
        '-tune', 'stillimage',
        '-profile:v', 'high',
        '-pix_fmt', 'yuv420p',
    ]
    common_audio = ['-c:a', 'aac', '-b:a', DEFAULT_AUDIO_BITRATE, '-ar', '44100', '-ac', '2']
    af_args = ['-af', 'aresample=async=1:first_pts=0,apad'] if has_audio else []

    command = [
        ffmpeg, '-y',
        *inputs,
        *video_args,
        *common_video,
        *af_args,
        *common_audio,
        '-t', duration_text,
        '-avoid_negative_ts', 'make_zero',
        '-movflags', '+faststart',
        output_path,
    ]

    _run_ffmpeg(command, timeout=timeout)


def _concat_segments(*, ffmpeg, segment_paths, output_path, fps, crf, preset, timeout):
    if len(segment_paths) == 1:
        shutil.copyfile(segment_paths[0], output_path)
        return

    command = [
        ffmpeg,
        '-y',
    ]
    for segment_path in segment_paths:
        command.extend(['-i', segment_path])

    concat_inputs = ''.join(f'[{index}:v:0][{index}:a:0]' for index in range(len(segment_paths)))
    command.extend(
        [
            '-filter_complex',
            f'{concat_inputs}concat=n={len(segment_paths)}:v=1:a=1[v][a]',
            '-map',
            '[v]',
            '-map',
            '[a]',
            '-r',
            str(fps),
            '-c:v',
            'libx264',
            '-preset',
            preset,
            '-crf',
            str(crf),
            '-profile:v',
            'high',
            '-pix_fmt',
            'yuv420p',
            '-c:a',
            'aac',
            '-b:a',
            DEFAULT_AUDIO_BITRATE,
            '-ar',
            '44100',
            '-ac',
            '2',
            '-movflags',
            '+faststart',
            output_path,
        ]
    )
    _run_ffmpeg(command, timeout=timeout)


def export_reel_video(project, frames, *, width=1080, height=1920, fps=30, crf=18, preset='', show_subtitles=False, subtitle_offset_percent=None):
    frame_items = list(frames or [])
    if not frame_items:
        raise VideoExportError('Aucune image de slide fournie pour exporter la video.')

    ffmpeg = _get_ffmpeg_executable()
    timeout = int(getattr(settings, 'REEL_VIDEO_FFMPEG_TIMEOUT_SECONDS', 900) or 900)
    resolved_preset = str(preset or getattr(settings, 'REEL_VIDEO_FFMPEG_PRESET', DEFAULT_VIDEO_PRESET) or DEFAULT_VIDEO_PRESET)
    slides_by_id = {slide.pk: slide for slide in project.slides.all()}
    segment_paths = []

    with tempfile.TemporaryDirectory(prefix='optitab-reel-video-') as temp_dir:

        for index, frame in enumerate(frame_items, start=1):
            slide_id = int(frame.get('slide_id') or 0)
            slide = slides_by_id.get(slide_id)
            if not slide:
                raise VideoExportError(f'Slide inconnue dans l export video: {slide_id}.')

            image_path = os.path.join(temp_dir, f'slide_{index:03d}.png')
            audio_path = os.path.join(temp_dir, f'slide_{index:03d}.mp3')
            segment_path = os.path.join(temp_dir, f'segment_{index:03d}.mp4')

            _save_frame_png(frame.get('image'), image_path, width=width, height=height)
            has_audio = _copy_audio_file(slide.speech_audio, audio_path) if slide.speech_audio else False
            segment_duration = _segment_duration(
                requested_duration=frame.get('duration_seconds') or slide.duration_seconds,
                audio_path=audio_path if has_audio else '',
                ffmpeg=ffmpeg,
                timeout=timeout,
            )

            subtitle_path = ''
            if show_subtitles and has_audio:
                ass_content = _build_ass_subtitles_for_slide(
                    slide,
                    width=width,
                    height=height,
                    segment_duration=segment_duration,
                    subtitle_offset_percent=subtitle_offset_percent,
                )
                if ass_content:
                    subtitle_path = os.path.join(temp_dir, f'subtitle_{index:03d}.ass')
                    with open(subtitle_path, 'w', encoding='utf-8') as fh:
                        fh.write(ass_content)

            _build_segment(
                ffmpeg=ffmpeg,
                image_path=image_path,
                audio_path=audio_path if has_audio else '',
                output_path=segment_path,
                duration=segment_duration,
                width=width,
                height=height,
                fps=fps,
                crf=crf,
                preset=resolved_preset,
                timeout=timeout,
                subtitle_path=subtitle_path,
            )
            segment_paths.append(segment_path)

        output_path = os.path.join(temp_dir, 'reel-export.mp4')
        _concat_segments(
            ffmpeg=ffmpeg,
            segment_paths=segment_paths,
            output_path=output_path,
            fps=fps,
            crf=crf,
            preset=resolved_preset,
            timeout=timeout,
        )

        if not os.path.exists(output_path) or os.path.getsize(output_path) <= 0:
            raise VideoExportError('FFmpeg a retourne une video vide.')

        with open(output_path, 'rb') as result:
            video_bytes = result.read()

    return {
        'video_bytes': video_bytes,
        'frame_count': len(frame_items),
        'width': width,
        'height': height,
        'fps': fps,
        'crf': crf,
        'preset': resolved_preset,
    }
