# -*- coding: utf-8 -*-
"""Convertit un fichier d'exercices (ancien format) au format OptiTAB v1.

Usage :
    python convertir_exercices.py <source.txt> <sortie.txt>

Le fichier garde sa structure (=== titre, Difficulté:, Image:, Énoncé:,
Étapes:, Solution:) : seuls les trois champs de contenu sont réécrits, chacun
précédé du marqueur <!-- optitab:1 -->. Un rapport des points à vérifier est
affiché (tableaux non convertis, étiquettes inconnues…).
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from optitab_v1 import (  # noqa: E402
    MARKER,
    convert_table_html,
    display_block,
    find_colon_outside_math,
    html_inline_to_text,
    math_only,
    math_spans,
    outside_math,
    top_level_relations,
    strip_displaystyle,
    strip_emojis,
    tidy_inline_math,
    tidy_statement_math,
)

SPACER_RE = re.compile(r"^(?:\$\s*(?:\\qquad|\\quad|\\,|\\;|\\ |~|\s)+\s*\$\s*)+")
LINEBREAK_RE = re.compile(r"\$\s*\\\\\s*\$")
QUESTION_RE = re.compile(r"^\*\*\s*Question\s+(\d+[a-z]?)\s*:?\s*\*\*\s*:?\s*(.*)$", re.I)
QUESTION_BOLD_RE = re.compile(r"^\*\*\s*Question\s+(\d+[a-z]?)\s*:\s*(.*?)\*\*\s*$", re.I)
BULLET_RE = re.compile(r"^●\s*(.*)$")
LABEL_RE = re.compile(r"^\*\*(.+?)\*\*\s*:?\s*(.*)$")
SUB_RE = re.compile(r"^[•▪◦]\s*(.*)$")
DASH_RE = re.compile(r"^[-–]\s+(.*)$")
IMAGE_RE = re.compile(r"^\[\s*IMAGE\s*_?\s*\d+\s*\]$", re.I)


def norm(s):
    return (
        s.lower()
        .replace("é", "e").replace("è", "e").replace("ê", "e").replace("à", "a")
        .replace("ù", "u").replace("ô", "o").replace("î", "i").replace("ç", "c")
    )


def classify_label(label):
    """Étiquette d'un point ● -> (type d'encadré, titre)."""
    lab = strip_emojis(label).strip().rstrip(":").strip()
    k = norm(lab)
    m = re.match(r"^etape\s*(\d+)?\s*:?\s*(.*)$", k)
    if m:
        rest = lab[len(lab) - len(m.group(2)):] if m.group(2) else ""
        return "etape", rest.strip()
    if re.match(r"^methode(\s*\d+)?$", k):
        return "methode", ""
    if k.startswith("methode"):
        return "methode", lab[len("Méthode"):].strip(" :")
    if re.match(r"^(resultat|resultats|conclusion|solution finale|solution|reponse|reponses|reponse finale)$", k):
        return "resultat", ""
    if k.startswith("remarque") or k in ("note", "idee", "explication", "a noter", "nota"):
        return "remarque", ""
    if k.startswith("attention") or k.startswith("erreur") or k.startswith("piege"):
        return "attention", ""
    if k in ("rappel", "formule", "formule a utiliser", "formules", "propriete", "proprietes",
             "propriete utilisee", "proprietes utilisees", "theoreme", "theoreme utilise", "definition"):
        title = "" if k == "rappel" else lab
        return "rappel", title
    if k.startswith("astuce") or k.startswith("conseil"):
        return "conseil", ""
    return "point", lab


def split_title_body(rest):
    rest = rest.strip()
    if not rest:
        return "", ""
    idx = find_colon_outside_math(rest)
    if idx is not None:
        left = rest[:idx].strip()
        right = rest[idx + 1:].strip()
        if left and len(outside_math(left).strip()) <= 70:
            return left, right
    if rest.endswith(":") and not rest.endswith("$:"):
        return rest[:-1].strip(), ""
    plain = outside_math(rest).strip()
    if len(plain) + 4 * len(re.findall(r"\$", rest)) // 2 <= 70 and len(rest) <= 110:
        return rest, ""
    return "", rest


def clean_line(raw):
    """Ligne brute -> (indentation, texte sans espaceurs, avait un espaceur)."""
    line = raw.replace("\t", "    ").rstrip()
    indent = len(line) - len(line.lstrip(" "))
    text = line.strip()
    had_spacer = False
    m = SPACER_RE.match(text)
    if m:
        had_spacer = True
        text = text[m.end():].strip()
    text = LINEBREAK_RE.sub(" ", text).strip()
    return indent, text, had_spacer


class Writer:
    """Assemble les lignes du format, avec gestion des encadrés ouverts."""

    def __init__(self, warnings):
        self.out = []
        self.block = None  # dict(kind, title, lines)
        self.warnings = warnings

    def blank(self):
        if self.out and self.out[-1] != "":
            self.out.append("")

    def open(self, kind, title):
        self.close()
        self.block = {"kind": kind, "title": title, "lines": []}

    def body(self, lines):
        target = self.block["lines"] if self.block else self.out
        target.extend(lines)

    def close(self):
        if not self.block:
            return
        b = self.block
        self.block = None
        lines = finalize_body(b["lines"])
        self.blank()
        head = f"::: {b['kind']}"
        if b["title"]:
            head += f" {tidy_inline_math(b['title'])}"
        self.out.append(head)
        self.out.extend(lines)
        self.out.append(":::")
        self.out.append("")

    def text(self):
        self.close()
        txt = "\n".join(self.out)
        txt = re.sub(r"\n{3,}", "\n\n", txt).strip()
        return txt


def item_math(item):
    """Contenu mathématique d'un élément formé uniquement de formules.

    « $A = B$ $= C$ » (formules juxtaposées sans texte) compte comme une
    seule formule « A = B = C ».
    """
    single = math_only(item)
    if single is not None:
        return single
    t = item.strip()
    spans = math_spans(t)
    if len(spans) < 2:
        return None
    if re.sub(r"\s+", "", outside_math(t)):
        return None
    parts = []
    for a, b in spans:
        seg = t[a:b]
        parts.append(seg[2:-2] if seg.startswith("$$") else seg[1:-1])
    return " ".join(p.strip() for p in parts)


def finalize_body(lines):
    """Post-traitement du corps d'un encadré : chaînes d'égalités, formules seules.

    Les éléments de liste consécutifs qui forment une chaîne de calcul
    (« $f'(x) = …$ » puis « $= …$ ») deviennent une seule formule alignée.
    """
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r"^- (.*)$", ln)
        if m:
            first = m.group(1)
            label = ""
            tex = item_math(first)
            if tex is None:
                idx = find_colon_outside_math(first)
                if idx is not None:
                    tail = item_math(first[idx + 1:])
                    if tail is not None and len(outside_math(first[:idx]).strip()) <= 30:
                        label = first[:idx].strip()
                        tex = tail
            chain = [strip_displaystyle(tex)] if tex is not None else None
            if chain is not None and len(top_level_relations(chain[0])) >= 2 and len(chain[0]) >= 55:
                # une seule puce, mais une longue chaîne d'égalités
                chain = [chain[0], ""]
            j = i + 1
            while chain is not None and j < len(lines):
                m2 = re.match(r"^- (.*)$", lines[j])
                if not m2:
                    break
                t2 = item_math(m2.group(1))
                if t2 is None:
                    break
                t2 = strip_displaystyle(t2)
                if not re.match(r"^(=|\\Leftrightarrow|\\iff|\\Longleftrightarrow)", t2):
                    break
                chain.append(t2)
                j += 1
            if chain is not None and len(chain) >= 2:
                if out and out[-1] != "":
                    out.append("")
                if label:
                    out.append(f"{label} :")
                    out.append("")
                joined = " ".join(c for c in chain if c)
                out.extend(display_block(joined, chain_min_len=0))
                out.append("")
                i = j
                continue
            out.append(f"- {tidy_inline_math(first)}")
            i += 1
            continue
        out.append(ln)
        i += 1
    # Corps réduit à une formule : formule centrée
    content = [x for x in out if x.strip()]
    if len(content) == 1 and not content[0].startswith(("- ", "  - ", "$$", "|", ":::", "[")):
        tex = math_only(content[0])
        if tex is not None:
            return display_block(tex)
    while out and out[-1] == "":
        out.pop()
    while out and out[0] == "":
        out.pop(0)
    return out


def convert_text_line(text):
    """Texte d'une ligne de contenu : HTML en ligne retiré, emojis retirés."""
    t = html_inline_to_text(text) if "<" in text else text
    t = strip_emojis(t)
    return t.strip()


def convert_statement(field, warnings):
    """Énoncé : introduction + questions numérotées."""
    w = Writer(warnings)
    lines = field.split("\n")
    i = 0
    in_question = False
    while i < len(lines):
        indent, text, _ = clean_line(lines[i])
        if not text:
            i += 1
            continue
        if text.lower().startswith("<table"):
            buf = [text]
            while "</table>" not in text.lower() and i + 1 < len(lines):
                i += 1
                text = lines[i].strip()
                buf.append(text)
            conv = convert_table_html("\n".join(buf), warnings)
            pad = "   " if in_question else ""
            w.blank()
            w.out.extend(pad + l for l in conv)
            w.blank()
            i += 1
            continue
        q = QUESTION_BOLD_RE.match(text) or QUESTION_RE.match(text)
        if q:
            body = convert_text_line(q.group(2))
            if not in_question:
                w.blank()
            w.out.append(f"{q.group(1)}. {tidy_statement_math(body)}")
            in_question = True
            i += 1
            continue
        if IMAGE_RE.match(text):
            w.blank() if not in_question else None
            w.out.append(("   " if in_question else "") + text.replace(" ", ""))
            i += 1
            continue
        t = convert_text_line(text)
        if t.startswith("●"):
            # indication rattachée à la question (« Formule à utiliser : … »)
            t = t[1:].strip()
        if not t:
            i += 1
            continue
        if in_question:
            w.out.append("")
            w.out.append("   " + tidy_statement_math(t))
        else:
            w.blank()
            w.out.append(tidy_statement_math(t))
        i += 1
    return w.text()


def convert_steps(field, warnings):
    """Étapes (corrigé détaillé) : questions, méthode, étapes, résultat."""
    w = Writer(warnings)
    lines = field.split("\n")
    i = 0
    last_sub = False
    while i < len(lines):
        indent, text, had_spacer = clean_line(lines[i])
        if not text:
            i += 1
            continue

        if text.lower().startswith("<table"):
            buf = [text]
            while "</table>" not in lines[i].lower() and i + 1 < len(lines):
                i += 1
                buf.append(lines[i].strip())
            conv = convert_table_html("\n".join(buf), warnings)
            if w.block:
                w.body(["", *conv, ""])
            else:
                w.blank()
                w.out.extend(conv)
                w.blank()
            last_sub = False
            i += 1
            continue

        q = QUESTION_BOLD_RE.match(text) or QUESTION_RE.match(text)
        if q:
            w.close()
            w.blank()
            body = convert_text_line(q.group(2))
            w.out.append(f"## Question {q.group(1)} : {tidy_statement_math(body)}")
            w.out.append("")
            last_sub = False
            i += 1
            continue

        if IMAGE_RE.match(text):
            w.close()
            w.blank()
            w.out.append(text.replace(" ", ""))
            w.out.append("")
            last_sub = False
            i += 1
            continue

        b = BULLET_RE.match(text)
        if b:
            content = b.group(1).strip()
            lab = LABEL_RE.match(content)
            if lab:
                kind, title = classify_label(lab.group(1))
                rest = convert_text_line(lab.group(2))
                if kind == "etape":
                    t2, body = split_title_body(rest)
                    title = title or t2
                    if title and not body and not t2:
                        body = rest if rest and rest != title else ""
                elif kind == "point":
                    body = rest
                    if body.endswith(":") and not body.endswith("$:"):
                        body = body[:-1].strip()
                else:
                    body = rest
                w.open(kind, title)
                if body:
                    w.body([tidy_inline_math(body)])
            else:
                w.close()
                w.blank()
                w.out.append(tidy_inline_math(convert_text_line(content)))
            last_sub = False
            i += 1
            continue

        t = convert_text_line(text)
        s = SUB_RE.match(t)
        d = DASH_RE.match(t)
        if s:
            item = s.group(1).strip()
            if w.block is None:
                if not (w.out and w.out[-1].startswith(("- ", "  - "))):
                    w.blank()
                w.out.append(f"- {tidy_inline_math(item)}")
            else:
                if w.block["lines"] and not w.block["lines"][-1].startswith(("- ", "  - ")):
                    w.body([""])
                w.body([f"- {item}"])
            last_sub = True
        elif d:
            item = d.group(1).strip()
            prefix = "  - " if last_sub else "- "
            if w.block is None:
                if not (w.out and w.out[-1].startswith(("- ", "  - "))):
                    w.blank()
                w.out.append(f"{prefix}{tidy_inline_math(item)}")
            else:
                w.body([f"{prefix}{tidy_inline_math(item)}"])
        else:
            if w.block is not None:
                prev_item = w.block["lines"] and w.block["lines"][-1].startswith(("- ", "  - "))
                cont_math = math_only(t) is not None and re.match(r"^\$\s*(\\displaystyle\s*)?(=|\\Leftrightarrow|\\iff)", t)
                if prev_item and (indent >= 8 or cont_math):
                    # suite d'un sous-point (ou suite d'une chaîne de calcul)
                    w.block["lines"][-1] += " " + t
                else:
                    w.body(["", tidy_inline_math(t)])
            else:
                w.blank()
                w.out.append(tidy_inline_math(t))
            last_sub = False
        i += 1
    return w.text()


def convert_solution(field, warnings):
    """Solution : réponses numérotées."""
    w = Writer(warnings)
    for raw in field.split("\n"):
        indent, text, _ = clean_line(raw)
        if not text:
            continue
        q = QUESTION_BOLD_RE.match(text) or QUESTION_RE.match(text)
        if q:
            w.out.append(f"{q.group(1)}. {tidy_inline_math(convert_text_line(q.group(2)))}")
            continue
        m = re.match(r"^(\d+[a-z]?)[.)]\s*(.*)$", text)
        if m:
            w.out.append(f"{m.group(1)}. {tidy_inline_math(convert_text_line(m.group(2)))}")
            continue
        if IMAGE_RE.match(text):
            w.blank()
            w.out.append(text.replace(" ", ""))
            w.blank()
            continue
        t = convert_text_line(text)
        if t:
            if w.out and re.match(r"^\d+[a-z]?\. ", w.out[-1]):
                w.out.append("")
                w.out.append("   " + tidy_inline_math(t))
            else:
                w.blank()
                w.out.append(tidy_inline_math(t))
    return w.text()


FIELD_RE = re.compile(r"^(Énoncé|Étapes|Solution):[ \t]*", re.M)


def convert_block(block, warnings):
    """Un exercice (texte entre deux === ) -> texte converti."""
    m_en = re.search(r"^Énoncé:", block, re.M)
    m_et = re.search(r"^Étapes:", block, re.M)
    m_so = re.search(r"^Solution:", block, re.M)
    if not (m_en and m_et and m_so):
        warnings.append("exercice sans les trois champs (laissé tel quel)")
        return block
    head = block[: m_en.start()].rstrip()
    enonce = block[m_en.end(): m_et.start()]
    etapes = block[m_et.end(): m_so.start()]
    solution = block[m_so.end():]
    parts = [
        head,
        "",
        "Énoncé:",
        MARKER,
        convert_statement(enonce, warnings),
        "",
        "Étapes:",
        MARKER,
        convert_steps(etapes, warnings),
        "",
        "Solution:",
        MARKER,
        convert_solution(solution, warnings),
    ]
    return "\n".join(parts)


def convert_file(src, dst):
    raw = Path(src).read_text(encoding="utf-8").replace("\r\n", "\n")
    chunks = re.split(r"^===[ \t]*$", raw, flags=re.M)
    out = []
    report = []
    for chunk in chunks:
        if not chunk.strip():
            continue
        title = chunk.strip().splitlines()[0]
        warnings = []
        out.append(convert_block(chunk.strip(), warnings))
        for wmsg in warnings:
            report.append(f"{title} : {wmsg}")
    text = "\n\n===\n\n".join(out) + "\n\n===\n"
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    Path(dst).write_text(text, encoding="utf-8")
    return len(out), report


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    count, report = convert_file(sys.argv[1], sys.argv[2])
    print(f"{count} exercices convertis -> {sys.argv[2]}")
    for r in report:
        print("  !", r)
