"""PDF rendering service for course content."""

from __future__ import annotations

import html
import logging
import re
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Any

from django.template.loader import render_to_string
from django.utils.text import slugify

logger = logging.getLogger(__name__)

PDF_TEMPLATE_NAME = "cours/pdf/course_pdf_document.html"
PDF_READY_FLAG = "__COURSE_PDF_READY__"
PLAYWRIGHT_TIMEOUT_MS = 90_000

_SCRIPT_TAG_RE = re.compile(r"(?is)<script\b[^>]*>.*?</script>")
_SCRIPT_OPEN_TAG_RE = re.compile(r"(?is)<script\b[^>]*>")
_STYLE_TAG_RE = re.compile(r"(?is)<style\b[^>]*>.*?</style>")
_IFRAME_TAG_RE = re.compile(r"(?is)<iframe\b[^>]*>.*?</iframe>")
_EVENT_HANDLER_RE = re.compile(r"(?i)\son[a-z0-9_-]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)")
_JS_PROTOCOL_RE = re.compile(r"(?i)(href|src)\s*=\s*(['\"])\s*javascript:[^'\"]*\2")
_HTML_TAG_RE = re.compile(r"<[a-zA-Z!/][^>]*>")
_DELIMITER_LINE_RE = re.compile(r"(?m)^\s*=+\s*$")
_META_LINE_RE = re.compile(r"^\s*([\w \-]+)\s*:\s*(.+?)\s*$")


class CoursePdfGenerationError(RuntimeError):
    """Raised when course PDF generation fails."""


def render_course_pdf_html(cours: Any, request: Any | None = None) -> str:
    """Builds normalized HTML document used for preview and PDF generation."""
    context = _build_template_context(cours=cours, request=request)
    return render_to_string(PDF_TEMPLATE_NAME, context)


def render_course_pdf_bytes(cours: Any, request: Any | None = None) -> bytes:
    """Renders a native PDF (real selectable text) with Playwright."""
    try:
        from playwright.sync_api import sync_playwright
    except Exception as exc:  # pragma: no cover - import depends on runtime env
        raise CoursePdfGenerationError(
            "Playwright est introuvable. Installez la dependance puis lancez: "
            "python -m playwright install chromium"
        ) from exc

    html_document = render_course_pdf_html(cours=cours, request=request)

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(args=["--disable-dev-shm-usage"])
            context = browser.new_context()
            page = context.new_page()
            try:
                page.set_content(
                    html_document,
                    wait_until="networkidle",
                    timeout=PLAYWRIGHT_TIMEOUT_MS,
                )
                page.wait_for_function(
                    f"() => window.{PDF_READY_FLAG} === true",
                    timeout=15_000,
                )
                page.emulate_media(media="print")
                pdf_bytes = page.pdf(
                    format="A4",
                    margin={
                        "top": "14mm",
                        "right": "12mm",
                        "bottom": "14mm",
                        "left": "12mm",
                    },
                    print_background=True,
                    display_header_footer=False,
                    prefer_css_page_size=True,
                )
            finally:
                try:
                    page.close()
                finally:
                    try:
                        context.close()
                    finally:
                        browser.close()
    except Exception as exc:
        logger.exception("Erreur de generation PDF pour le cours %s", getattr(cours, "pk", None))
        message = str(exc)
        if "Executable doesn't exist" in message:
            raise CoursePdfGenerationError(
                "Chromium Playwright n'est pas installe. Lancez: python -m playwright install chromium"
            ) from exc
        raise CoursePdfGenerationError(f"Erreur Playwright: {message}") from exc

    return pdf_bytes


def build_course_pdf_filename(cours: Any) -> str:
    """Returns a stable, user-friendly file name for generated PDFs."""
    notion = getattr(cours, "notion", None)
    title = str(getattr(cours, "titre", "") or "").strip()
    if not title:
        try:
            metadata, _ = _extract_metadata_and_body(str(getattr(cours, "contenu", "") or ""))
            title = str(metadata.get("title", "") or "").strip()
        except Exception:
            title = ""
    if not title:
        title = str(getattr(notion, "titre", "") or "").strip()
    if not title:
        title = f"cours-{getattr(cours, 'pk', 'document')}"

    fallback = f"cours-{getattr(cours, 'pk', 'document')}"
    filename_stem = slugify(title) or fallback
    return f"{filename_stem}.pdf"


def _build_template_context(cours: Any, request: Any | None = None) -> dict[str, Any]:
    raw_source = str(getattr(cours, "contenu", "") or "")
    metadata, body_html = _extract_metadata_and_body(raw_source)
    cleaned_body_html = _sanitize_course_html(body_html)

    notion = getattr(cours, "notion", None)
    notion_title = str(getattr(notion, "titre", "") or "").strip()
    title = (
        metadata.get("title")
        or str(getattr(cours, "titre", "") or "").strip()
        or notion_title
        or "Cours OptiTAB"
    )
    description = metadata.get("description", "")
    difficulty = metadata.get("difficulty", "")
    order = metadata.get("order", "")

    subtitle_parts = []
    if notion_title and notion_title != title:
        subtitle_parts.append(notion_title)
    if description:
        subtitle_parts.append(description)

    meta_parts = []
    if difficulty:
        meta_parts.append(f"Difficulte: {difficulty}")
    if order:
        meta_parts.append(f"Ordre: {order}")

    base_url = "http://localhost:8000/"
    if request is not None:
        try:
            base_url = request.build_absolute_uri("/")
        except Exception:
            pass

    return {
        "cours": cours,
        "pdf_title": title,
        "pdf_subtitle": " | ".join(subtitle_parts),
        "pdf_meta_line": " | ".join(meta_parts),
        "course_body_html": cleaned_body_html,
        "base_url": base_url,
        "pdf_styles": _load_asset("static/cours/css/course_pdf_print.css"),
        "pdf_renderer_script": _load_asset("static/cours/js/course_pdf_renderer.js"),
    }


def _extract_metadata_and_body(raw_source: str) -> tuple[dict[str, str], str]:
    source = (raw_source or "").replace("\r\n", "\n").replace("\r", "\n").strip("\ufeff \n\t")
    if not source:
        return {}, "<p class='pdf-empty'>Aucun contenu n'est disponible pour ce cours.</p>"

    first_tag_match = _HTML_TAG_RE.search(source)
    if first_tag_match:
        prelude = source[: first_tag_match.start()]
        html_body = source[first_tag_match.start() :]
    else:
        prelude = source
        html_body = ""

    metadata = _parse_metadata(prelude)

    if html_body:
        body = _DELIMITER_LINE_RE.sub("", html_body).strip()
        if body:
            return metadata, body

    plain_text = _DELIMITER_LINE_RE.sub("", source).strip()
    return metadata, _plain_text_to_html(plain_text)


def _parse_metadata(prelude: str) -> dict[str, str]:
    metadata: dict[str, str] = {}

    for line in (prelude or "").splitlines():
        stripped = line.strip()
        if not stripped or stripped == "===":
            continue
        match = _META_LINE_RE.match(stripped)
        if not match:
            if "headline" not in metadata:
                metadata["headline"] = stripped
            continue
        key = _normalize_meta_key(match.group(1))
        value = match.group(2).strip()
        if not value:
            continue
        metadata[key] = value

    if "title" not in metadata and metadata.get("headline"):
        metadata["title"] = metadata["headline"]

    return metadata


def _normalize_meta_key(raw_key: str) -> str:
    normalized = unicodedata.normalize("NFKD", raw_key or "")
    normalized = normalized.encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-z0-9]+", "_", normalized.casefold()).strip("_")

    aliases = {
        "titre": "title",
        "title": "title",
        "description": "description",
        "difficulte": "difficulty",
        "difficulty": "difficulty",
        "ordre": "order",
        "order": "order",
    }
    return aliases.get(normalized, normalized)


def _plain_text_to_html(text: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text or "") if block.strip()]
    if not blocks:
        return "<p class='pdf-empty'>Aucun contenu n'est disponible pour ce cours.</p>"

    rendered_blocks = []
    for block in blocks:
        escaped = html.escape(block).replace("\n", "<br>")
        rendered_blocks.append(f"<p>{escaped}</p>")
    return "\n".join(rendered_blocks)


def _sanitize_course_html(raw_html: str) -> str:
    content = raw_html or ""
    content = _SCRIPT_TAG_RE.sub("", content)
    content = _SCRIPT_OPEN_TAG_RE.sub("", content)
    content = _STYLE_TAG_RE.sub("", content)
    content = _IFRAME_TAG_RE.sub("", content)
    content = _EVENT_HANDLER_RE.sub("", content)
    content = _JS_PROTOCOL_RE.sub(r"\1='#'", content)
    return content


@lru_cache(maxsize=8)
def _load_asset(relative_path: str) -> str:
    app_dir = Path(__file__).resolve().parents[1]
    asset_path = app_dir / relative_path
    try:
        return asset_path.read_text(encoding="utf-8")
    except Exception:
        logger.exception("Impossible de lire l'asset PDF: %s", asset_path)
        return ""
