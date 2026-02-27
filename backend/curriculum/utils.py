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


def resolve_exercice_title(exercice):
    title = str(getattr(exercice, "titre", "") or "").strip()
    if title:
        return title
    notion = getattr(exercice, "notion", None)
    return str(getattr(notion, "titre", "") or "").strip()


def resolve_exercice_image_alt(image_obj, exercice_title=""):
    alt_text = str(getattr(image_obj, "alt_text", "") or "").strip()
    if alt_text:
        return alt_text

    legende = str(getattr(image_obj, "legende", "") or "").strip()
    if legende:
        return legende

    filename = humanize_filename(getattr(getattr(image_obj, "image", None), "name", ""))
    if exercice_title and filename:
        return f"{exercice_title} - {filename}"
    if exercice_title:
        return f"{exercice_title} - illustration"
    if filename:
        return filename
    return "Illustration d'exercice"


def resolve_exercice_image_title(image_obj):
    title_text = str(getattr(image_obj, "title_text", "") or "").strip()
    if title_text:
        return title_text
    return humanize_filename(getattr(getattr(image_obj, "image", None), "name", ""))


def resolve_exercice_image_dimensions(image_obj):
    width = getattr(image_obj, "width", None)
    height = getattr(image_obj, "height", None)

    if width and height:
        return width, height

    image_field = getattr(image_obj, "image", None)
    try:
        if not width:
            width = int(getattr(image_field, "width", 0) or 0)
        if not height:
            height = int(getattr(image_field, "height", 0) or 0)
    except Exception:
        pass

    return (width or None, height or None)


def build_exercice_image_payload(image_obj, request=None, exercice_title=""):
    legende = str(getattr(image_obj, "legende", "") or "").strip()
    raw_alt = str(getattr(image_obj, "alt_text", "") or "").strip()
    raw_title = str(getattr(image_obj, "title_text", "") or "").strip()
    resolved_alt = resolve_exercice_image_alt(image_obj, exercice_title=exercice_title)
    resolved_title = resolve_exercice_image_title(image_obj)
    width, height = resolve_exercice_image_dimensions(image_obj)

    return {
        "id": image_obj.id,
        "image": build_public_image_url(getattr(image_obj, "image", None), request=request),
        "image_type": getattr(image_obj, "image_type", "") or "",
        "position": getattr(image_obj, "position", None),
        "legende": legende,
        "caption": legende,
        "alt_text": raw_alt,
        "title_text": raw_title,
        "alt_text_resolved": resolved_alt,
        "title_text_resolved": resolved_title,
        "width": width,
        "height": height,
    }
