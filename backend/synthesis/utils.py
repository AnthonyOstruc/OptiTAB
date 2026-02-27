import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


def humanize_filename(filename_or_path):
    raw = str(filename_or_path or "").strip()
    if not raw:
        return ""
    stem = Path(raw).stem
    cleaned = re.sub(r"[_\-]+", " ", stem)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    if not cleaned:
        return ""
    return cleaned[0].upper() + cleaned[1:]


def strip_url_query(url):
    raw = str(url or "").strip()
    if not raw:
        return ""
    parsed = urlsplit(raw)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, "", ""))


def build_public_image_url(image_field, request=None):
    if not image_field:
        return ""

    try:
        raw_url = str(getattr(image_field, "url", "") or "")
    except Exception:
        return ""

    if not raw_url:
        return ""

    clean_url = strip_url_query(raw_url)
    if request and not clean_url.startswith(("http://", "https://")):
        try:
            return strip_url_query(request.build_absolute_uri(clean_url))
        except Exception:
            return clean_url
    return clean_url


def resolve_synthesis_title(sheet):
    title = str(getattr(sheet, "titre", "") or "").strip()
    if title:
        return title
    notion = getattr(sheet, "notion", None)
    return str(getattr(notion, "titre", "") or "").strip()


def resolve_synthesis_image_alt(image_obj, synthesis_title=""):
    alt_text = str(getattr(image_obj, "alt_text", "") or "").strip()
    if alt_text:
        return alt_text

    caption = str(getattr(image_obj, "caption", "") or "").strip()
    if caption:
        return caption

    filename = humanize_filename(getattr(getattr(image_obj, "image", None), "name", ""))
    if synthesis_title and filename:
        return f"{synthesis_title} - {filename}"
    if synthesis_title:
        return f"{synthesis_title} - illustration"
    if filename:
        return filename
    return "Illustration de synthese"


def resolve_synthesis_image_title(image_obj):
    title_text = str(getattr(image_obj, "title_text", "") or "").strip()
    if title_text:
        return title_text
    return humanize_filename(getattr(getattr(image_obj, "image", None), "name", ""))


def resolve_synthesis_image_dimensions(image_obj):
    # Never trigger storage reads (S3) at render time.
    width = getattr(image_obj, "width", None)
    height = getattr(image_obj, "height", None)

    try:
        width = int(width) if width else None
    except (TypeError, ValueError):
        width = None
    try:
        height = int(height) if height else None
    except (TypeError, ValueError):
        height = None

    return width, height


def build_synthesis_image_payload(image_obj, request=None, synthesis_title=""):
    caption = str(getattr(image_obj, "caption", "") or "").strip()
    raw_alt = str(getattr(image_obj, "alt_text", "") or "").strip()
    raw_title = str(getattr(image_obj, "title_text", "") or "").strip()
    resolved_alt = resolve_synthesis_image_alt(image_obj, synthesis_title=synthesis_title)
    resolved_title = resolve_synthesis_image_title(image_obj)
    width, height = resolve_synthesis_image_dimensions(image_obj)

    return {
        "id": image_obj.id,
        "image": build_public_image_url(getattr(image_obj, "image", None), request=request),
        "image_type": getattr(image_obj, "image_type", "") or "",
        "position": getattr(image_obj, "position", None),
        "caption": caption,
        "legende": caption,
        "alt_text": raw_alt,
        "title_text": raw_title,
        "alt_text_resolved": resolved_alt,
        "title_text_resolved": resolved_title,
        "width": width,
        "height": height,
    }
