# -*- coding: utf-8 -*-
"""Contrôle de syntaxe des contenus au format OptiTAB v1.

Usage :
    python valider_v1.py <fichier> [<fichier> …]

Fichier d'exercices (=== titre … Énoncé: / Étapes: / Solution:) ou fichier
de cours / fiche (en-tête puis contenu). Contrôles : marqueur présent,
encadrés équilibrés et de type connu, tableaux tkz-tab cohérents, « $ »
appariés ligne par ligne, aucune balise HTML (sauf <br>), images [IMAGE_N]
déclarées dans l'en-tête Image(s):.
"""
import re
import sys
from pathlib import Path

MARKER_RE = re.compile(r"^\s*<!--\s*optitab:1\s*-->")
KINDS = {
    "definition", "theoreme", "propriete", "methode", "attention", "exemple",
    "demonstration", "remarque", "retenir", "rappel", "notation", "formule",
    "resultat", "etape", "point", "objectifs", "prerequis", "conseil", "tableau",
}
FENCE_OPEN = re.compile(r"^(:{3,})\s*([^\s:]\S*)\s*(.*)$")
FENCE_CLOSE = re.compile(r"^:{3,}\s*$")
SIGN_TOKENS = {"", "+", "-", "z", "d", "t", "h", "||"}
SIGN_WORD_RE = re.compile(r"^[A-Za-zÀ-ÖØ-öø-ÿ'’\- ]{3,}$")
VAR_RE = re.compile(r"^(R/?|[+=-]/.*|D[+-]/.*|[+-]D/.*|[+-]D[+-](/.*)?|[+-][CH]/.+)$")


def dollars(line):
    n = 0
    i = 0
    while i < len(line):
        if line[i] == "\\" and i + 1 < len(line):
            i += 2
            continue
        if line[i] == "$":
            n += 1
        i += 1
    return n


def split_top(s):
    parts, depth, buf = [], 0, ""
    for c in s:
        if c in "{([":
            depth += 1
        elif c in "})]" and depth:
            depth -= 1
        if c == "," and depth == 0:
            parts.append(buf.strip())
            buf = ""
        else:
            buf += c
    parts.append(buf.strip())
    return parts


def check_doc(text, where, problems, images_declared=None):
    if not MARKER_RE.match(text):
        problems.append(f"{where} : marqueur <!-- optitab:1 --> absent")
        return
    lines = text.split("\n")[1:]
    stack = []
    in_display = False
    in_code = False
    table = None
    used_images = set()
    for no, raw in enumerate(lines, start=2):
        line = raw.strip()
        loc = f"{where} l.{no}"
        if table is not None:
            if FENCE_CLOSE.match(line):
                check_table(table, loc, problems)
                table = None
                stack.pop()
                continue
            if line:
                table.append(line)
            continue
        if in_display:
            if line.endswith("$$"):
                in_display = False
            continue
        if in_code:
            if line.startswith("```"):
                in_code = False
            continue
        if line.startswith("```"):
            in_code = True
            continue
        if FENCE_OPEN.match(line):
            kind = FENCE_OPEN.match(line).group(2)
            k = kind.lower()
            if k not in KINDS and k not in ("savoirfaire", "erreur", "astuce", "conclusion", "verification", "variations", "signes"):
                problems.append(f"{loc} : type d'encadré inconnu « {kind} »")
            stack.append(k)
            if k in ("tableau", "variations", "signes"):
                table = []
            continue
        if FENCE_CLOSE.match(line):
            if not stack:
                problems.append(f"{loc} : ::: fermant sans ouverture")
            else:
                stack.pop()
            continue
        if line.startswith("$$") and not (line.endswith("$$") and len(line) > 4):
            in_display = True
            continue
        if re.search(r"<(?!br\s*/?>)[a-zA-Z/][^>]*>", line):
            problems.append(f"{loc} : balise HTML « {re.search(r'<[^>]*>', line).group(0)[:40]} »")
        if dollars(line) % 2:
            problems.append(f"{loc} : « $ » non apparié : {line[:70]}")
        for m in re.finditer(r"\[\s*IMAGE\s*_?\s*(\d+)\s*\]", line, re.I):
            used_images.add(int(m.group(1)))
    if stack:
        problems.append(f"{where} : {len(stack)} encadré(s) non fermé(s) ({', '.join(stack)})")
    if in_display:
        problems.append(f"{where} : formule $$ non fermée")
    if in_code:
        problems.append(f"{where} : bloc de code ``` non fermé")
    if images_declared is not None:
        for k in sorted(used_images):
            if k > images_declared:
                problems.append(f"{where} : [IMAGE_{k}] utilisée mais {images_declared} image(s) déclarée(s)")


def check_table(rows, loc, problems):
    parsed = []
    for r in rows:
        m = re.match(r"^(.+?)\s*:\s*(.*)$", r)
        if not m:
            problems.append(f"{loc} : ligne de tableau sans « : » : {r[:50]}")
            return
        parsed.append((m.group(1), split_top(m.group(2))))
    if not parsed:
        problems.append(f"{loc} : tableau vide")
        return
    n = len(parsed[0][1])
    for label, entries in parsed[1:]:
        if len(entries) == 2 * n - 1:
            bad = [e for k, e in enumerate(entries)
                   if k % 2 == 1 and e not in SIGN_TOKENS and not e.startswith(("\\", "$"))
                   and not SIGN_WORD_RE.match(e)]
            if bad:
                problems.append(f"{loc} : signes inattendus dans « {label} » : {bad}")
        elif len(entries) == n:
            bad = [e for e in entries if not VAR_RE.match(e.replace(" ", ""))]
            if bad:
                problems.append(f"{loc} : variations mal écrites dans « {label} » : {bad}")
        else:
            problems.append(f"{loc} : « {label} » a {len(entries)} éléments (attendu {n} ou {2 * n - 1})")


def check_file(path, problems):
    raw = Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")
    name = Path(path).name
    if re.search(r"^Énoncé:", raw, re.M):
        for block in re.split(r"^===[ \t]*$", raw, flags=re.M):
            block = block.strip()
            if not block:
                continue
            title = block.splitlines()[0].replace("===", "").strip()
            im = re.search(r"^Images?:\s*(.+)$", block, re.M)
            n_img = len([s for s in im.group(1).split(",") if s.strip()]) if im else 0
            for field, nxt in (("Énoncé", "Étapes"), ("Étapes", "Solution"), ("Solution", None)):
                s = block.find(f"{field}:")
                e = block.find(f"{nxt}:", s) if nxt else len(block)
                if s < 0:
                    problems.append(f"{name} « {title} » : rubrique {field} absente")
                    continue
                check_doc(block[s + len(field) + 1: e].strip(), f"{name} « {title[:40]} » {field}", problems, n_img)
        return
    start = raw.find("<!--")
    check_doc(raw[start:] if start >= 0 else raw, name, problems)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    problems = []
    for f in sys.argv[1:]:
        check_file(f, problems)
    for p in problems:
        print("  ✗", p)
    print(f"{len(sys.argv) - 1} fichier(s) contrôlé(s), {len(problems)} problème(s)")
    sys.exit(1 if problems else 0)
