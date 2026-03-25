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
_EMPTY_BODY_HTML = "<p class='pdf-empty'>Aucun contenu n'est disponible pour ce cours.</p>"

_SCRIPT_TAG_RE = re.compile(r"(?is)<script\b[^>]*>.*?</script>")
_SCRIPT_OPEN_TAG_RE = re.compile(r"(?is)<script\b[^>]*>")
_STYLE_TAG_RE = re.compile(r"(?is)<style\b[^>]*>.*?</style>")
_IFRAME_TAG_RE = re.compile(r"(?is)<iframe\b[^>]*>.*?</iframe>")
_EVENT_HANDLER_RE = re.compile(r"(?i)\son[a-z0-9_-]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)")
_JS_PROTOCOL_RE = re.compile(r"(?i)(href|src)\s*=\s*(['\"])\s*javascript:[^'\"]*\2")
_HTML_TAG_RE = re.compile(r"<[a-zA-Z!/][^>]*>")
_HTML_TAG_NAME_RE = re.compile(r"(?is)<\s*/?\s*([a-z0-9]+)\b")
_DELIMITER_LINE_RE = re.compile(r"(?m)^\s*=+\s*$")
_META_LINE_RE = re.compile(r"^\s*([\w \-]+)\s*:\s*(.+?)\s*$")
_BLOCK_DELIMITER_RE = re.compile(r"^\s*=+\s*(.*?)\s*$")
_QUESTION_LINE_RE = re.compile(
    r"^\s*(?:\*\*)?\s*question\s*(\d+)?\s*[:\-]\s*(.+?)\s*(?:\*\*)?\s*$",
    re.IGNORECASE,
)
_EXERCISE_LINE_RE = re.compile(
    r"^\s*(?:\*\*)?\s*(?:exercice|sujet)\s*(\d+)?\s*[:\-]?\s*(.*?)\s*(?:\*\*)?\s*$",
    re.IGNORECASE,
)
_MARKDOWN_HEADING_RE = re.compile(r"^\s*(#{2,4})\s+(.+?)\s*$")
_ORDERED_ITEM_RE = re.compile(r"^\s*(\d+)[\.\)]\s+(.+?)\s*$")
_UNORDERED_ITEM_RE = re.compile(r"^\s*(?:[-*\u2022\u25cf\u25e6\u25aa])\s+(.+?)\s*$")
_SPACER_LINE_RE = re.compile(r"^\s*(?:\$\\+\$|\\+)\s*$")
_SECTION_LINE_RE = re.compile(r"^\s*([^:]+?)\s*:\s*(.*?)\s*$")
_BRACKET_SECTION_RE = re.compile(r"^\s*\[([^\]]+)\]\s*$")
_INLINE_MEDIA_BLOCK_RE = re.compile(r"(?is)<figure\b[^>]*>.*?</figure>|<img\b[^>]*>")
_INLINE_MEDIA_TOKEN_RE = re.compile(r"^\s*\[\[HTML_BLOCK_(\d+)\]\]\s*$")
_STRUCTURED_TEXT_CUE_RE = re.compile(
    r"(?im)^\s*(?:={3,}|\**\s*(?:titre|difficulte|difficulty|ordre|description|enonce|énoncé|etapes|étapes|solution|correction|corrige|question\s+\d+)\s*:)"
)
_INLINE_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
_INLINE_CODE_RE = re.compile(r"`([^`]+)`")
_INLINE_ITALIC_RE = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")

_ALLOWED_META_KEYS = {
    "title",
    "description",
    "difficulty",
    "order",
    "images",
    "image",
    "niveau",
    "matiere",
    "serie",
    "type",
    "duree",
    "points",
    "competences",
    "objectif",
    "objectifs",
    "classe",
    "chapitre",
    "session",
    "annee",
    "chapitre",
    "notion",
    "sous_notion",
    "sousnotion",
    "type_exercice",
    "type_d_exercice",
    "temps_estime",
    "objectif_pedagogique",
    "objectif_pedagogique_principal",
    "prerequis",
    "erreurs_frequentes",
    "competences_visees",
}
_ANNAL_SECTION_META = {
    "objectif": ("Objectif", "note"),
    "objectifs": ("Objectifs", "note"),
    "objectif_pedagogique": ("Objectif pedagogique", "note"),
    "objectif_pedagogique_principal": ("Objectif pedagogique principal", "note"),
    "prerequis": ("Prerequis", "note"),
    "erreurs_frequentes": ("Erreurs frequentes", "note"),
    "competences": ("Competences", "note"),
    "competences_visees": ("Competences visees", "note"),
    "consigne": ("Consigne", "statement"),
    "enonce": ("Enonce", "statement"),
    "enonce_eleve": ("Enonce eleve", "statement"),
    "enonce_du_sujet": ("Enonce", "statement"),
    "sujet": ("Sujet", "statement"),
    "questions": ("Questions", "questions"),
    "questions_progressives": ("Questions progressives", "questions"),
    "etapes": ("Etapes", "method"),
    "etape": ("Etapes", "method"),
    "decoupage_pedagogique": ("Decoupage pedagogique", "method"),
    "etapes_de_resolution": ("Etapes de resolution", "method"),
    "methode": ("Methode", "method"),
    "demarche": ("Demarche", "method"),
    "indices": ("Indices", "note"),
    "indices_progressifs": ("Indices progressifs", "note"),
    "aides_progressives": ("Aides progressives", "note"),
    "aides": ("Aides", "note"),
    "correction_detaillee": ("Correction detaillee", "correction"),
    "correction_pedagogique_detaillee": ("Correction pedagogique detaillee", "correction"),
    "solution": ("Solution", "solution"),
    "correction": ("Correction", "solution"),
    "corrige": ("Corrige", "solution"),
    "reponses_finales": ("Reponses finales", "final"),
    "reponse_finale": ("Reponse finale", "final"),
    "resultats_attendus": ("Resultats attendus", "final"),
    "reponse": ("Reponse", "solution"),
    "bareme": ("Bareme", "note"),
    "a_retenir": ("A retenir", "final"),
    "retenir": ("A retenir", "final"),
    "prolongement": ("Prolongement", "note"),
    "bonus": ("Bonus", "note"),
    "astuce": ("Astuce", "note"),
    "astuces": ("Astuces", "note"),
    "conseil": ("Conseil", "note"),
    "conseils": ("Conseils", "note"),
    "rappel": ("Rappel", "note"),
}


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
    exercise_count = metadata.get("exercise_count", "")
    niveau = str(metadata.get("niveau", "")).strip()
    matiere = str(metadata.get("matiere", "")).strip()
    annale_type = str(metadata.get("type", "")).strip()
    duree = str(metadata.get("duree", "")).strip()
    points = str(metadata.get("points", "")).strip()
    chapitre = str(metadata.get("chapitre", "")).strip()
    notion = str(metadata.get("notion", "")).strip()

    subtitle_parts = []
    if notion_title and notion_title != title:
        subtitle_parts.append(notion_title)
    if description:
        subtitle_parts.append(description)

    meta_parts = []
    if difficulty:
        _, difficulty_label = _humanize_difficulty(difficulty)
        meta_parts.append(f"Difficulte: {difficulty_label or difficulty}")
    if niveau:
        meta_parts.append(f"Niveau: {niveau}")
    if matiere:
        meta_parts.append(f"Matiere: {matiere}")
    if annale_type:
        meta_parts.append(f"Type: {annale_type}")
    if duree:
        meta_parts.append(f"Duree: {duree}")
    if points:
        meta_parts.append(f"Points: {points}")
    if chapitre:
        meta_parts.append(f"Chapitre: {chapitre}")
    if notion:
        meta_parts.append(f"Notion: {notion}")
    if order:
        meta_parts.append(f"Ordre: {order}")
    if exercise_count:
        meta_parts.append(f"Exercices: {exercise_count}")

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
        return {}, _EMPTY_BODY_HTML

    if _looks_like_structured_text_source(source):
        source_without_media, inline_media_blocks = _replace_inline_media_blocks(source)
        metadata, body_html = _parse_plain_text_source(source_without_media)
        return metadata, _restore_inline_media_blocks(body_html, inline_media_blocks)

    first_tag_match = _HTML_TAG_RE.search(source)
    if first_tag_match:
        prelude = source[: first_tag_match.start()]
        html_body = source[first_tag_match.start() :]
        metadata = _parse_metadata(prelude)
        prelude_body_html = ""
        if prelude.strip():
            prelude_metadata, prelude_body_html = _parse_plain_text_source(prelude)
            metadata = {**prelude_metadata, **metadata}
        body = _DELIMITER_LINE_RE.sub("", html_body).strip()
        if prelude_body_html and prelude_body_html != _EMPTY_BODY_HTML:
            body = f"{prelude_body_html}\n{body}".strip()
        if body:
            return metadata, body
        if prelude_body_html:
            return metadata, prelude_body_html
        return metadata, _EMPTY_BODY_HTML

    return _parse_plain_text_source(source)


def _looks_like_structured_text_source(source: str) -> bool:
    return bool(_STRUCTURED_TEXT_CUE_RE.search(source or ""))


def _replace_inline_media_blocks(source: str) -> tuple[str, dict[str, str]]:
    inline_media_blocks: dict[str, str] = {}
    counter = 1

    def replace(match: re.Match[str]) -> str:
        nonlocal counter
        token = f"[[HTML_BLOCK_{counter}]]"
        inline_media_blocks[token] = match.group(0)
        counter += 1
        return token

    source_without_media = _INLINE_MEDIA_BLOCK_RE.sub(replace, source or "")
    return source_without_media, inline_media_blocks


def _restore_inline_media_blocks(rendered_html: str, inline_media_blocks: dict[str, str]) -> str:
    html_output = rendered_html or ""
    for token, block_html in inline_media_blocks.items():
        html_output = html_output.replace(f"<p>{token}</p>", block_html)
        html_output = html_output.replace(token, block_html)
    return html_output


def _is_inline_media_token(value: str) -> bool:
    return bool(_INLINE_MEDIA_TOKEN_RE.match(value or ""))


def _contains_html_fragment(value: str) -> bool:
    return bool(_HTML_TAG_NAME_RE.search(value or ""))


def _format_rich_text(value: str) -> str:
    if _contains_html_fragment(value):
        return value or ""
    return _format_inline_text(value)


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
        "niveau": "niveau",
        "classe": "classe",
        "niveau_scolaire": "niveau",
        "matiere": "matiere",
        "matiere_nom": "matiere",
        "chapitre": "chapitre",
        "notion": "notion",
        "sous_notion": "sous_notion",
        "sousnotion": "sous_notion",
        "serie": "serie",
        "type": "type",
        "type_exercice": "type",
        "type_d_exercice": "type",
        "duree": "duree",
        "duree_estimee": "duree",
        "temps_estime": "duree",
        "temps": "duree",
        "points": "points",
        "competence": "competences",
        "competences": "competences",
        "competences_visees": "competences_visees",
        "objectif": "objectif",
        "objectifs": "objectifs",
        "objectif_pedagogique": "objectif_pedagogique",
        "objectif_pedagogique_principal": "objectif_pedagogique_principal",
        "prerequis": "prerequis",
        "erreurs_frequentes": "erreurs_frequentes",
        "session": "session",
        "annee": "annee",
        "enonce": "enonce",
        "consigne": "consigne",
        "questions": "questions",
        "etape": "etapes",
        "etapes": "etapes",
        "methode": "methode",
        "demarche": "demarche",
        "correction": "correction",
        "corrige": "corrige",
        "correction_detaillee": "correction_detaillee",
        "reponse": "reponse",
        "reponse_finale": "reponse_finale",
        "reponses_finales": "reponses_finales",
        "resultats_attendus": "resultats_attendus",
        "bareme": "bareme",
    }
    return aliases.get(normalized, normalized)


def _plain_text_to_html(text: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text or "") if block.strip()]
    if not blocks:
        return _EMPTY_BODY_HTML

    rendered_blocks = []
    for block in blocks:
        if _is_inline_media_token(block):
            rendered_blocks.append(block)
            continue
        escaped = html.escape(block).replace("\n", "<br>")
        rendered_blocks.append(f"<p>{escaped}</p>")
    return "\n".join(rendered_blocks)


def _parse_plain_text_source(source: str) -> tuple[dict[str, str], str]:
    blocks = _split_text_blocks(source)
    parsed_blocks: list[dict[str, Any]] = []

    for block in blocks:
        parsed = _parse_text_block(block.get("title", ""), block.get("lines", []))
        if parsed["body_lines"] or parsed["title"] or parsed["metadata"]:
            parsed_blocks.append(parsed)

    if not parsed_blocks:
        return {}, _EMPTY_BODY_HTML

    metadata = dict(parsed_blocks[0]["metadata"])
    if parsed_blocks[0]["title"] and "title" not in metadata:
        metadata["title"] = parsed_blocks[0]["title"]

    if len(parsed_blocks) > 1 or any(_block_has_annale_cues(block) for block in parsed_blocks):
        metadata["exercise_count"] = str(len(parsed_blocks))
        return metadata, _render_annale_blocks(parsed_blocks)

    body_html = _render_basic_text_lines(parsed_blocks[0]["body_lines"])
    if not body_html.strip():
        body_html = _EMPTY_BODY_HTML
    return metadata, body_html


def _split_text_blocks(source: str) -> list[dict[str, Any]]:
    lines = (source or "").splitlines()
    if not lines:
        return [{"title": "", "lines": []}]

    blocks: list[dict[str, Any]] = []
    current_lines: list[str] = []
    current_title = ""
    encountered_delimiter = False

    for raw_line in lines:
        match = _BLOCK_DELIMITER_RE.match(raw_line)
        if match:
            delimiter_payload = (match.group(1) or "").strip()
            has_explicit_title = bool(delimiter_payload and set(delimiter_payload) != {"="})
            if has_explicit_title or raw_line.strip() == "===":
                encountered_delimiter = True
                if current_lines or current_title:
                    blocks.append({"title": current_title, "lines": current_lines})
                    current_lines = []
                current_title = _clean_block_title(delimiter_payload)
                continue
        current_lines.append(raw_line)

    if current_lines or current_title or not encountered_delimiter:
        blocks.append({"title": current_title, "lines": current_lines})

    return blocks or [{"title": "", "lines": lines}]


def _clean_block_title(raw_title: str) -> str:
    title = (raw_title or "").strip()
    if title.startswith("[") and title.endswith("]"):
        title = title[1:-1].strip()
    return title


def _parse_text_block(block_title: str, lines: list[str]) -> dict[str, Any]:
    metadata: dict[str, str] = {}
    body_lines: list[str] = []
    in_body = False

    for raw_line in lines:
        stripped = raw_line.strip()

        if not in_body:
            if not stripped:
                continue

            meta_match = _META_LINE_RE.match(stripped)
            if meta_match:
                key = _normalize_meta_key(meta_match.group(1))
                value = meta_match.group(2).strip()
                if key in _ALLOWED_META_KEYS and value:
                    metadata[key] = value
                    continue

            in_body = True

        body_lines.append(raw_line)

    title = metadata.get("title") or (block_title or "").strip()
    if title:
        metadata["title"] = title

    return {
        "title": title,
        "metadata": metadata,
        "body_lines": body_lines,
    }


def _block_has_annale_cues(block: dict[str, Any]) -> bool:
    searchable = "\n".join(block.get("body_lines", []))
    normalized = unicodedata.normalize("NFKD", searchable).encode("ascii", "ignore").decode("ascii").casefold()
    return any(
        cue in normalized
        for cue in (
            "question",
            "consigne",
            "enonce",
            "questions",
            "prerequis",
            "aides_progressives",
            "etapes",
            "solution",
            "correction",
            "corrige",
            "reponses_finales",
            "bareme",
        )
    )


def _render_annale_blocks(blocks: list[dict[str, Any]]) -> str:
    if not blocks:
        return _EMPTY_BODY_HTML

    html_parts = ["<section class='annale-document'>"]

    if len(blocks) > 1:
        html_parts.append(
            "<div class='annale-summary'>"
            f"<strong>Annale d'exercices :</strong> {len(blocks)} exercices structures"
            "</div>"
        )

    for index, block in enumerate(blocks, start=1):
        metadata = block.get("metadata", {})
        title = str(block.get("title") or f"Exercice {index}").strip()
        description = str(metadata.get("description", "")).strip()
        difficulty_key, difficulty_label = _humanize_difficulty(str(metadata.get("difficulty", "")).strip())
        order = str(metadata.get("order", "")).strip()
        annale_type = str(metadata.get("type", "")).strip()
        niveau = str(metadata.get("niveau", "")).strip()
        matiere = str(metadata.get("matiere", "")).strip()
        chapitre = str(metadata.get("chapitre", "")).strip()
        notion = str(metadata.get("notion", "")).strip()
        sous_notion = str(metadata.get("sous_notion", "")).strip()
        serie = str(metadata.get("serie", "")).strip()
        duree = str(metadata.get("duree", "")).strip()
        points = str(metadata.get("points", "")).strip()
        prerequis = str(metadata.get("prerequis", "")).strip()
        erreurs_frequentes = str(metadata.get("erreurs_frequentes", "")).strip()
        objectifs = str(
            metadata.get("objectifs")
            or metadata.get("objectif")
            or metadata.get("objectif_pedagogique")
            or metadata.get("objectif_pedagogique_principal")
            or ""
        ).strip()
        competences = str(metadata.get("competences") or metadata.get("competences_visees") or "").strip()
        body_html = _render_annale_body(block.get("body_lines", []))
        if not body_html.strip():
            body_html = "<p class='pdf-empty'>Aucun enonce n'est disponible pour cet exercice.</p>"

        html_parts.append("<article class='annale-card'>")
        html_parts.append("<header class='annale-card-header'>")
        html_parts.append(
            f"<p class='annale-card-index'>Exercice {index}</p>"
            f"<h2 class='annale-card-title'>{html.escape(title)}</h2>"
        )

        badges: list[str] = []
        if difficulty_label:
            badges.append(
                "<span class='annale-badge annale-badge--difficulty "
                f"annale-badge--{html.escape(difficulty_key)}'>{html.escape(difficulty_label)}</span>"
            )
        if annale_type:
            badges.append(
                "<span class='annale-badge annale-badge--type'>Type: "
                f"{html.escape(annale_type)}</span>"
            )
        if niveau:
            badges.append(
                "<span class='annale-badge annale-badge--niveau'>Niveau: "
                f"{html.escape(niveau)}</span>"
            )
        if matiere:
            badges.append(
                "<span class='annale-badge annale-badge--matiere'>Matiere: "
                f"{html.escape(matiere)}</span>"
            )
        if serie:
            badges.append(
                "<span class='annale-badge annale-badge--serie'>Serie: "
                f"{html.escape(serie)}</span>"
            )
        if duree:
            badges.append(
                "<span class='annale-badge annale-badge--duree'>Duree: "
                f"{html.escape(duree)}</span>"
            )
        if points:
            badges.append(
                "<span class='annale-badge annale-badge--points'>Points: "
                f"{html.escape(points)}</span>"
            )
        if order:
            badges.append(
                "<span class='annale-badge annale-badge--order'>Ordre: "
                f"{html.escape(order)}</span>"
            )
        if badges:
            html_parts.append(f"<div class='annale-badges'>{''.join(badges)}</div>")

        if description:
            html_parts.append(f"<p class='annale-card-description'>{html.escape(description)}</p>")
        if chapitre:
            html_parts.append(
                "<p class='annale-card-context'><strong>Chapitre :</strong> "
                f"{html.escape(chapitre)}</p>"
            )
        if notion:
            html_parts.append(
                "<p class='annale-card-context'><strong>Notion :</strong> "
                f"{html.escape(notion)}</p>"
            )
        if sous_notion:
            html_parts.append(
                "<p class='annale-card-context'><strong>Sous-notion :</strong> "
                f"{html.escape(sous_notion)}</p>"
            )
        if objectifs:
            html_parts.append(
                "<p class='annale-card-context'><strong>Objectifs :</strong> "
                f"{html.escape(objectifs)}</p>"
            )
        if competences:
            html_parts.append(
                "<p class='annale-card-context'><strong>Competences :</strong> "
                f"{html.escape(competences)}</p>"
            )
        if prerequis:
            html_parts.append(
                "<p class='annale-card-context'><strong>Prerequis :</strong> "
                f"{html.escape(prerequis)}</p>"
            )
        if erreurs_frequentes:
            html_parts.append(
                "<p class='annale-card-context'><strong>Erreurs frequentes :</strong> "
                f"{html.escape(erreurs_frequentes)}</p>"
            )
        html_parts.append("</header>")

        html_parts.append(f"<div class='annale-card-body'>{body_html}</div>")
        html_parts.append("</article>")

    html_parts.append("</section>")
    return "\n".join(html_parts)


def _render_basic_text_lines(lines: list[str]) -> str:
    text = "\n".join(lines).strip()
    if not text:
        return ""
    return _plain_text_to_html(text)


def _render_annale_body(lines: list[str]) -> str:
    if not lines:
        return ""

    html_parts: list[str] = []
    paragraph_lines: list[str] = []
    list_kind: str | None = None
    list_items: list[str] = []
    section_open = False
    section_body_open = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if not paragraph_lines:
            return
        content = "<br>".join(paragraph_lines).strip()
        if content:
            html_parts.append(f"<p>{content}</p>")
        paragraph_lines = []

    def flush_list() -> None:
        nonlocal list_kind, list_items
        if not list_items:
            return
        tag = "ol" if list_kind == "ol" else "ul"
        css_class = "annale-list annale-list--ordered" if tag == "ol" else "annale-list annale-list--bullet"
        joined = "".join(f"<li>{item}</li>" for item in list_items)
        html_parts.append(f"<{tag} class='{css_class}'>{joined}</{tag}>")
        list_kind = None
        list_items = []

    def close_section() -> None:
        nonlocal section_open, section_body_open
        flush_paragraph()
        flush_list()
        if section_body_open:
            html_parts.append("</div>")
            section_body_open = False
        if section_open:
            html_parts.append("</section>")
            section_open = False

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if not stripped:
            flush_paragraph()
            flush_list()
            continue

        if _is_inline_media_token(stripped):
            flush_paragraph()
            flush_list()
            html_parts.append(stripped)
            continue

        if _SPACER_LINE_RE.match(stripped):
            flush_paragraph()
            flush_list()
            html_parts.append("<div class='annale-spacer' aria-hidden='true'></div>")
            continue

        heading_match = _MARKDOWN_HEADING_RE.match(stripped)
        if heading_match:
            flush_paragraph()
            flush_list()
            level = min(max(len(heading_match.group(1)), 2), 4)
            title = _format_inline_text(heading_match.group(2))
            html_parts.append(f"<h{level}>{title}</h{level}>")
            continue

        bracket_section_match = _BRACKET_SECTION_RE.match(stripped)
        if bracket_section_match:
            flush_paragraph()
            flush_list()
            section_key = _normalize_meta_key(bracket_section_match.group(1))
            section_meta = _ANNAL_SECTION_META.get(section_key)
            if section_meta:
                close_section()
                section_label, section_css_suffix = section_meta
                html_parts.append(f"<section class='annale-section annale-section--{section_css_suffix}'>")
                html_parts.append(f"<h3 class='annale-section-title'>{html.escape(section_label)}</h3>")
                html_parts.append("<div class='annale-section-body'>")
                section_open = True
                section_body_open = True
                continue
            html_parts.append(f"<h3>{_format_inline_text(bracket_section_match.group(1))}</h3>")
            continue

        section_match = _SECTION_LINE_RE.match(stripped)
        if section_match:
            section_key = _normalize_meta_key(section_match.group(1))
            section_meta = _ANNAL_SECTION_META.get(section_key)
            if section_meta:
                close_section()
                section_label, section_css_suffix = section_meta
                html_parts.append(f"<section class='annale-section annale-section--{section_css_suffix}'>")
                html_parts.append(f"<h3 class='annale-section-title'>{html.escape(section_label)}</h3>")
                html_parts.append("<div class='annale-section-body'>")
                section_open = True
                section_body_open = True
                payload = section_match.group(2).strip()
                if payload:
                    paragraph_lines.append(_format_rich_text(payload))
                continue

        question_match = _QUESTION_LINE_RE.match(stripped)
        if question_match:
            flush_paragraph()
            flush_list()
            number = question_match.group(1)
            title = _format_rich_text(question_match.group(2))
            label = f"Question {number}" if number else "Question"
            html_parts.append(
                "<div class='annale-question'>"
                f"<p class='annale-question-label'>{html.escape(label)}</p>"
                f"<p class='annale-question-text'>{title}</p>"
                "</div>"
            )
            continue

        exercise_match = _EXERCISE_LINE_RE.match(stripped)
        if exercise_match and (exercise_match.group(1) or exercise_match.group(2)):
            flush_paragraph()
            flush_list()
            number = exercise_match.group(1)
            detail = _format_rich_text(exercise_match.group(2))
            title = f"Exercice {number}" if number else "Exercice"
            detail_html = f" : {detail}" if detail else ""
            html_parts.append(
                "<div class='annale-exercice-line'>"
                f"<strong>{html.escape(title)}</strong>{detail_html}"
                "</div>"
            )
            continue

        if _contains_html_fragment(stripped):
            flush_paragraph()
            flush_list()
            html_parts.append(stripped)
            continue

        ordered_match = _ORDERED_ITEM_RE.match(stripped)
        if ordered_match:
            flush_paragraph()
            if list_kind not in {None, "ol"}:
                flush_list()
            list_kind = "ol"
            list_items.append(_format_rich_text(ordered_match.group(2)))
            continue

        unordered_match = _UNORDERED_ITEM_RE.match(stripped)
        if unordered_match:
            flush_paragraph()
            if list_kind not in {None, "ul"}:
                flush_list()
            list_kind = "ul"
            list_items.append(_format_rich_text(unordered_match.group(1)))
            continue

        if list_items:
            if re.match(r"^\s{2,}\S", line):
                list_items[-1] = f"{list_items[-1]}<br>{_format_rich_text(stripped)}"
                continue
            flush_list()

        paragraph_lines.append(_format_rich_text(_strip_wrapping_markdown(stripped)))

    close_section()
    flush_paragraph()
    flush_list()
    return "\n".join(html_parts)


def _humanize_difficulty(raw_value: str) -> tuple[str, str]:
    normalized = (raw_value or "").strip().casefold()
    mapping = {
        "easy": ("easy", "Facile"),
        "facile": ("easy", "Facile"),
        "medium": ("medium", "Moyen"),
        "moyen": ("medium", "Moyen"),
        "intermediaire": ("medium", "Moyen"),
        "hard": ("hard", "Difficile"),
        "difficile": ("hard", "Difficile"),
    }
    return mapping.get(normalized, ("", ""))


def _strip_wrapping_markdown(value: str) -> str:
    text = (value or "").strip()
    if len(text) >= 4 and text.startswith("**") and text.endswith("**"):
        return text[2:-2].strip()
    return text


def _format_inline_text(value: str) -> str:
    escaped = html.escape(value or "")
    escaped = _INLINE_CODE_RE.sub(r"<code>\1</code>", escaped)
    escaped = _INLINE_BOLD_RE.sub(r"<strong>\1</strong>", escaped)
    escaped = _INLINE_ITALIC_RE.sub(r"<em>\1</em>", escaped)
    return escaped


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
