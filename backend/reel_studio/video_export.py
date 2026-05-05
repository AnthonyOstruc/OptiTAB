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
):
    vf = _video_filter(width, height)
    duration_text = f'{duration:.3f}'
    common_video = [
        '-vf',
        vf,
        '-r',
        str(fps),
        '-c:v',
        'libx264',
        '-preset',
        preset,
        '-crf',
        str(crf),
        '-tune',
        'stillimage',
        '-profile:v',
        'high',
        '-pix_fmt',
        'yuv420p',
    ]
    common_audio = ['-c:a', 'aac', '-b:a', DEFAULT_AUDIO_BITRATE, '-ar', '44100', '-ac', '2']

    if audio_path:
        command = [
            ffmpeg,
            '-y',
            '-loop',
            '1',
            '-framerate',
            str(fps),
            '-t',
            duration_text,
            '-i',
            image_path,
            '-i',
            audio_path,
            '-map',
            '0:v:0',
            '-map',
            '1:a:0',
            *common_video,
            '-af',
            'aresample=async=1:first_pts=0,apad',
            *common_audio,
            '-t',
            duration_text,
            '-avoid_negative_ts',
            'make_zero',
            '-movflags',
            '+faststart',
            output_path,
        ]
    else:
        command = [
            ffmpeg,
            '-y',
            '-loop',
            '1',
            '-framerate',
            str(fps),
            '-t',
            duration_text,
            '-i',
            image_path,
            '-f',
            'lavfi',
            '-t',
            duration_text,
            '-i',
            'anullsrc=channel_layout=stereo:sample_rate=44100',
            '-map',
            '0:v:0',
            '-map',
            '1:a:0',
            *common_video,
            *common_audio,
            '-t',
            duration_text,
            '-avoid_negative_ts',
            'make_zero',
            '-movflags',
            '+faststart',
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


def export_reel_video(project, frames, *, width=1080, height=1920, fps=30, crf=18, preset=''):
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
