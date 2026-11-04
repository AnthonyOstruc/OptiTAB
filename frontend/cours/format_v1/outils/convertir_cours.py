# -*- coding: utf-8 -*-
"""Convertit un cours ou une fiche (HTML historique) au format OptiTAB v1.

Usage :
    python convertir_cours.py <source.txt> <sortie.txt>

Les lignes d'en-tête (Titre:, Description:, Images:…) placées avant le premier
`<` sont conservées ; le contenu HTML est converti en texte structuré précédé
du marqueur <!-- optitab:1 -->. Les encadrés sont reconnus d'après leur
étiquette (« Définition - … », « À retenir », « Méthode »…), à défaut d'après
leur couleur (palette frontend/cours/cours_optitab/PALETTE_COULEURS.txt).
"""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from optitab_v1 import (  # noqa: E402
    MARKER,
    Node,
    chain_relations,
    code_fence,
    code_from_html,
    convert_table_html,
    display_block,
    is_code_style,
    html_inline_to_text,
    math_only,
    parse_html,
    strip_emojis,
    tidy_inline_math,
)

# (fond, bordure, type) — d'après la palette des cours
COLOR_KINDS = [
    ("#e8f4fd", "#3498db", "definition"),
    ("#f3e5f5", "#9c27b0", "propriete"),
    ("#fef3c7", "#f59e0b", "methode"),
    ("#f8f9fa", "#6c757d", "exemple"),
    ("#ecfdf5", "#10b981", "remarque"),
    ("#fff8dc", "#ffa500", "attention"),
    ("#fee2e2", "#dc2626", "attention"),
    ("#e0f2f1", "#00897b", "demonstration"),
    ("#e0f7fa", "#00acc1", "notation"),
    ("#eef2ff", "#4f46e5", "formule"),
    ("#f0f9f0", None, "retenir"),
    ("#e8f5e8", None, "resultat"),
    ("#ecfdf5", None, "resultat"),
    ("#fff3cd", "#ffc107", "attention"),
    ("#f0f8ff", "#87ceeb", "rappel"),
    ("#f8f9fa", "#3498db", "definition"),
    ("#ffffff", "#6c757d", "exemple"),
    ("#fef3c7", None, "methode"),
    ("#e8f5e9", None, "retenir"),
    ("#e3f2fd", None, "definition"),
    ("#ffebee", None, "attention"),
    ("#f8f9fa", None, "exemple"),
]

LABEL_KINDS = [
    (r"[ée]tapes?", "etape"),
    (r"d[ée]finitions?", "definition"),
    (r"th[ée]or[èe]mes?", "theoreme"),
    (r"propri[ée]t[ée]s?", "propriete"),
    (r"m[ée]thodes?", "methode"),
    (r"exemples?", "exemple"),
    (r"d[ée]monstrations?|preuve", "demonstration"),
    (r"remarques?", "remarque"),
    (r"attention|erreurs?(?: fr[ée]quentes?)?(?: à éviter)?|pi[èe]ges?", "attention"),
    (r"notations?", "notation"),
    (r"(?:à|a) retenir|l['’]essentiel|essentiel", "retenir"),
    (r"r[ée]sultats?|solutions?|r[ée]ponses?|conclusions?", "resultat"),
    (r"conseils?(?: m[ée]thodologiques?)?|astuces?", "conseil"),
    (r"rappels?", "rappel"),
    (r"principe", "methode"),
    (r"objectifs?", "objectifs"),
    (r"pr[ée]requis", "prerequis"),
]

IMAGE_RE = re.compile(r"\[\s*IMAGE\s*_?\s*\d+\s*\]", re.I)
BR = " "


def style_of(node):
    return node.style


def box_kind_by_color(st):
    bg = re.search(r"background(?:-color)?:(#[0-9a-f]{3,6})", st)
    bl = re.search(r"border-left:\d+px(?:solid)?(#[0-9a-f]{3,6})", st)
    bgc = bg.group(1) if bg else None
    blc = bl.group(1) if bl else None
    for fond, bord, kind in COLOR_KINDS:
        if bgc == fond and (bord is None or blc == bord or bord in st):
            return kind
    return None


def label_to_kind(label, fallback):
    clean = strip_emojis(label).strip().rstrip(":").strip()
    clean = re.sub(r"\s+", " ", clean)
    for pat, kind in LABEL_KINDS:
        m = re.match(rf"^(?:{pat})\b", clean, re.I)
        if m:
            raw_rest = clean[m.end():].strip()
            named = bool(re.match(r"^[-–—:]", raw_rest))
            rest = re.sub(r"^[-–—:]\s*", "", raw_rest).strip()
            if not rest or re.fullmatch(r"\d+[a-z]?", rest):
                return kind, ""
            # « Méthode générale », « Objectif pédagogique », « Exemples d'utilisation » :
            # simple qualificatif, l'étiquette suffit
            if not named and (" " not in rest or re.match(r"^(d'|de |des |du )", rest, re.I)) and rest[:1].islower():
                return kind, ""
            return kind, rest[0].upper() + rest[1:]
    return fallback or "remarque", clean


def is_card(st):
    return ("background:#ffffff" in st or "background:#fff;" in st or "background:white" in st) and "border:1px" in st


def is_wrapper(st):
    return "background:#f9f9f9" in st or not re.search(r"background", st)


def inline_text(fragment):
    s = re.sub(r"<br\s*/?>", BR, fragment, flags=re.I)
    t = html_inline_to_text(s)
    t = re.sub(r"[ \t\r\n]+", " ", t)
    return strip_emojis(t).strip()


def para_lines(text):
    """Paragraphe -> lignes : formule seule = formule centrée."""
    out = []
    for piece in text.split(BR):
        p = piece.strip()
        if not p:
            continue
        if IMAGE_RE.fullmatch(p):
            out += ["", p.replace(" ", ""), ""]
            continue
        tex = math_only(p)
        if tex is not None:
            out += ["", *display_block(tex), ""]
        else:
            out += ["", tidy_inline_math(p), ""]
    return out


def list_lines(node, depth=0):
    out = []
    ordered = node.tag == "ol"
    k = 0
    for li in node.elements():
        if li.tag != "li":
            continue
        k += 1
        nested = [c for c in li.elements() if c.tag in ("ul", "ol")]
        own = "".join(
            c.outer_html() if isinstance(c, Node) and c.tag not in ("ul", "ol")
            else (html.escape(c, quote=False) if isinstance(c, str) else "")
            for c in li.children
        )
        text = inline_text(own).replace(BR, " ")
        marker = f"{k}." if ordered else "-"
        out.append("  " * depth + f"{marker} {tidy_inline_math(text)}")
        for sub in nested:
            out.extend(list_lines(sub, depth + 1))
    return ["", *out, ""]


def extract_label(node):
    """Retire l'étiquette en tête d'un encadré ; renvoie son texte (ou '')."""
    for idx, c in enumerate(node.children):
        if isinstance(c, str):
            if c.strip():
                return ""
            continue
        if c.tag in ("strong", "b"):
            node.children.pop(idx)
            return c.text()
        if c.tag == "p":
            els = c.elements()
            if els and els[0].tag in ("strong", "b"):
                lead = els[0]
                before = "".join(x for x in c.children[: c.children.index(lead)] if isinstance(x, str))
                if before.strip():
                    return ""
                label = lead.text()
                c.children.remove(lead)
                if not c.text().strip():
                    node.children.pop(idx)
                return label
            return ""
        if c.tag in ("h3", "h4"):
            node.children.pop(idx)
            return c.text()
        return ""
    return ""


def convert_nodes(node, warnings):
    lines = []
    buf = []

    def flush():
        if buf:
            text = inline_text("".join(buf))
            buf.clear()
            if text:
                lines.extend(para_lines(text))

    for c in node.children:
        if isinstance(c, str):
            buf.append(html.escape(c, quote=False))
            continue
        tag = c.tag
        if tag in ("strong", "b", "em", "i", "span", "a", "sup", "sub", "code", "br"):
            buf.append(c.outer_html())
            continue
        flush()
        if tag == "p":
            lines.extend(para_lines(inline_text(c.html())))
        elif tag in ("ul", "ol"):
            lines.extend(list_lines(c))
        elif tag == "table":
            lines += ["", *convert_table_html(c.outer_html(), warnings), ""]
        elif tag in ("h1", "h2"):
            lines += ["", f"## {inline_text(c.html())}", ""]
        elif tag == "h3":
            lines += ["", f"### {inline_text(c.html())}", ""]
        elif tag in ("h4", "h5", "h6"):
            lines += ["", f"#### {inline_text(c.html())}", ""]
        elif tag == "div":
            lines.extend(convert_div(c, warnings))
        elif tag == "pre":
            lines.extend(code_fence(code_from_html(c.html())))
        elif tag in ("hr",):
            continue
        elif tag == "img":
            warnings.append("image HTML directe (à remplacer par [IMAGE_N])")
        else:
            lines.extend(convert_nodes(c, warnings))
    flush()
    return lines


CALC_RE = re.compile(r"background:#(ffffff|fff|e8f5e8|ecfdf5|f0fdf4);?.*border-left:4pxsolid#6c757d")


def convert_div(div, warnings):
    st = style_of(div)
    if is_code_style(st):
        return code_fence(code_from_html(div.html()))
    if CALC_RE.search(st):
        # ligne de calcul encadrée (« 5(x+3) = … », puis « = 5x + 15 ») : formule centrée,
        # les lignes successives sont ensuite réunies en une formule alignée
        texte = inline_text(div.html())
        tex = math_only(texte)
        if tex is not None:
            return ["", f"$${tex}$$", ""]
    if "border:3px" in st or "border:2.5px" in st:
        body = convert_nodes(div, warnings)
        return ["", "::: formule", *strip_blank(body), ":::", ""]
    if is_card(st) or is_wrapper(st):
        return convert_nodes(div, warnings)
    color_kind = box_kind_by_color(st)
    label = extract_label(div)
    if label:
        kind, title = label_to_kind(label, color_kind)
    else:
        kind, title = (color_kind or "remarque"), ""
        if not color_kind:
            warnings.append(f"encadré de couleur inconnue ({st[:60]})")
    body = polish_body(strip_blank(convert_nodes(div, warnings)))
    if kind == "etape" and not title and body:
        first = body[0].strip()
        if len(first) <= 70 and not first.endswith(".") and not first.startswith(("-", "$$", "|", ":::", "[")):
            title = first
            body = strip_blank(body[1:])
    if kind == "resultat" and len([x for x in body if x.strip()]) == 1:
        tex = math_only(body[0]) if body else None
        if tex is not None:
            body = display_block(tex)
    head = f"::: {kind}" + (f" {tidy_inline_math(title)}" if title else "")
    return ["", head, *body, ":::", ""]


def polish_body(lines):
    """Corps d'encadré : puces « • » -> liste, majuscule initiale."""
    out = []
    for ln in lines:
        m = re.match(r"^[•●▪]\s*(.*)$", ln.strip())
        if m:
            if out and out[-1] == "" and len(out) >= 2 and out[-2].startswith("- "):
                out.pop()
            out.append(f"- {m.group(1)}")
        else:
            out.append(ln)
    for k, ln in enumerate(out):
        if ln.strip():
            first = ln.lstrip()
            if first[:1].islower() and not first.startswith(("- ", "$")):
                out[k] = ln[: len(ln) - len(first)] + first[0].upper() + first[1:]
            break
    return out


def strip_blank(lines):
    out = list(lines)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    # pas plus d'une ligne vide d'affilée
    res = []
    for ln in out:
        if not ln.strip() and res and not res[-1].strip():
            continue
        res.append(ln)
    return res


def attach_orphan_tables(lines):
    """Encadré vide suivi d'un tableau : le tableau entre dans l'encadré."""
    out = list(lines)
    i = 0
    while i < len(out) - 1:
        if out[i].startswith("::: ") and out[i + 1].strip() == ":::":
            j = i + 2
            while j < len(out) and not out[j].strip():
                j += 1
            if j < len(out) and out[j].startswith("|"):
                k = j
                while k < len(out) and out[k].startswith("|"):
                    k += 1
                table = out[j:k]
                out[i + 1:k] = table + [":::"]
        i += 1
    return out


def keycap_lists(lines):
    """« 1⃣ texte » (chiffres-emojis) -> liste numérotée « 1. texte »."""
    out = []
    for ln in lines:
        m = re.match(r"^(\s*)(\d)️?⃣\s*(.*)$", ln)
        if m:
            if out and not out[-1].strip() and len(out) >= 2 and re.match(r"^\s*\d+\. ", out[-2]):
                out.pop()
            out.append(f"{m.group(1)}{m.group(2)}. {m.group(3)}")
        else:
            out.append(ln)
    return out


def box_inline_examples(lines):
    """Paragraphe « **Exemples :** … » hors encadré -> encadré Exemple."""
    out = []
    depth = 0
    for ln in lines:
        s = ln.strip()
        if re.match(r"^:{3,}\s*\S", s):
            depth += 1
        elif re.match(r"^:{3,}\s*$", s):
            depth = max(0, depth - 1)
        m = re.match(r"^\*\*\s*Exemples?\s*:?\s*\*\*\s*:?\s*(.+)$", s)
        if m and depth == 0:
            body = m.group(1).strip()
            out += ["::: exemple", body[0].upper() + body[1:] if body[:1].islower() else body, ":::"]
            continue
        out.append(ln)
    return out


def merge_display_chains(lines):
    """$$A = B$$ puis $$= C$$ (lignes séparées) -> une formule alignée."""
    out = []
    i = 0
    single = re.compile(r"^\$\$(.+)\$\$$")
    while i < len(lines):
        m = single.match(lines[i].strip())
        if not m:
            out.append(lines[i])
            i += 1
            continue
        chain = [m.group(1).strip()]
        j = i + 1
        while True:
            k = j
            while k < len(lines) and not lines[k].strip():
                k += 1
            m2 = single.match(lines[k].strip()) if k < len(lines) else None
            if not m2 or not re.match(r"^(=|\\Leftrightarrow|\\iff|\\Rightarrow)", m2.group(1).strip()):
                break
            chain.append(m2.group(1).strip())
            j = k + 1
        if len(chain) > 1:
            out += display_block(" ".join(chain), chain_min_len=0)
            i = j
        else:
            out.append(lines[i])
            i += 1
    return out


def convert_html(html_text, warnings):
    root = parse_html(html_text)
    lines = merge_display_chains(keycap_lists(box_inline_examples(attach_orphan_tables(strip_blank(convert_nodes(root, warnings))))))
    txt = "\n".join(lines)
    txt = re.sub(r"\n{3,}", "\n\n", txt)
    return MARKER + "\n" + txt.strip() + "\n"


def convert_file(src, dst):
    raw = Path(src).read_text(encoding="utf-8").replace("\r\n", "\n")
    start = raw.find("<")
    header = raw[:start].rstrip() if start > 0 else ""
    warnings = []
    body = convert_html(raw[start:] if start >= 0 else raw, warnings)
    out = (header + "\n\n" if header else "") + body
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(out, encoding="utf-8")
    return warnings


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    report = convert_file(sys.argv[1], sys.argv[2])
    print(f"converti -> {sys.argv[2]}")
    for r in report:
        print("  !", r)
