# -*- coding: utf-8 -*-
"""Outils communs du format OptiTAB v1 (conversion de l'ancien contenu).

Le format est décrit dans frontend/cours/format_v1/FORMAT.md et rendu par
frontend/src/utils/optitabDoc.js. Ce module ne dépend que de la bibliothèque
standard : analyse des formules, conversion des tableaux HTML (tableaux de
variations -> syntaxe tkz-tab), nettoyage des balises et des emojis.
"""
import html
import re
from html.parser import HTMLParser

MARKER = "<!-- optitab:1 -->"

# ---------------------------------------------------------------------------
#  Formules
# ---------------------------------------------------------------------------

EMOJI_RE = re.compile(
    "[\U0001F300-\U0001FAFF\u2600-\u27BF\u2B50\u2B06\u2B07\u2B05\u27A1\uFE0F\u200D\u2705\u274C\u2714\u2716]"
)


def strip_emojis(text):
    t = re.sub(r"\s{2,}", " ", EMOJI_RE.sub("", text)).strip()
    return french_quotes(t)


def french_quotes(text):
    """Guillemets droits "…" -> « … » (hors formules)."""
    if '"' not in text:
        return text
    out = []
    last = 0
    for a, b in math_spans(text):
        out.append(re.sub(r'"\s*(?:\*\*)?\s*([^"]+?)\s*(?:\*\*)?\s*"', lambda m: f"« {m.group(1).strip()} »", text[last:a]))
        out.append(text[a:b])
        last = b
    out.append(re.sub(r'"\s*(?:\*\*)?\s*([^"]+?)\s*(?:\*\*)?\s*"', lambda m: f"« {m.group(1).strip()} »", text[last:]))
    return "".join(out)


def math_spans(text):
    """Liste des (début, fin) des formules $…$ / $$…$$ (hors \\$)."""
    spans = []
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n:
            i += 2
            continue
        if c == "$":
            delim = "$$" if text.startswith("$$", i) else "$"
            j = i + len(delim)
            end = -1
            while j < n:
                if text[j] == "\\":
                    j += 2
                    continue
                if text.startswith(delim, j):
                    end = j
                    break
                j += 1
            if end < 0:
                break
            spans.append((i, end + len(delim)))
            i = end + len(delim)
            continue
        i += 1
    return spans


def outside_math(text):
    """Texte hors formules (formules remplacées par un espace)."""
    out = []
    last = 0
    for a, b in math_spans(text):
        out.append(text[last:a])
        out.append(" ")
        last = b
    out.append(text[last:])
    return "".join(out)


def math_only(text):
    """Si le texte est exactement une formule $…$, renvoie son contenu."""
    t = text.strip()
    spans = math_spans(t)
    if len(spans) == 1 and spans[0] == (0, len(t)):
        inner = t[2:-2] if t.startswith("$$") else t[1:-1]
        return inner.strip()
    return None


def strip_displaystyle(tex):
    return re.sub(r"\\displaystyle\s*", "", tex).strip()


def tidy_statement_math(text):
    """Énoncés : fractions en grand format, sauf dans une longue phrase."""
    return tidy_inline_math(text, prose_threshold=60, single_only=False)


def tidy_inline_math(text, prose_threshold=25, single_only=True):
    """Retire \\displaystyle des formules noyées dans une phrase.

    Une formule seule (ou précédée d'une courte étiquette) garde son style
    « display » ; dans une vraie phrase, les fractions reprennent la taille
    du texte et l'interlignage reste régulier.
    """
    prose = re.sub(r"[\s:;,.!?()\-–]+", "", outside_math(text))
    if len(prose) < prose_threshold and (not single_only or len(math_spans(text)) <= 1):
        return text
    out = []
    last = 0
    for a, b in math_spans(text):
        out.append(text[last:a])
        seg = text[a:b]
        if not seg.startswith("$$"):
            seg = "$" + strip_displaystyle(seg[1:-1]) + "$"
        out.append(seg)
        last = b
    out.append(text[last:])
    return "".join(out)


def find_colon_outside_math(text):
    spans = math_spans(text)
    for i, c in enumerate(text):
        if c != ":":
            continue
        if any(a <= i < b for a, b in spans):
            continue
        before = text[i - 1] if i > 0 else " "
        after = text[i + 1] if i + 1 < len(text) else " "
        if before.isspace() or after.isspace():
            return i
    return None


ARROWS = ("\\Leftrightarrow", "\\iff", "\\Longleftrightarrow", "\\Rightarrow", "\\implies", "\\Longrightarrow")


def chain_relations(tex):
    """Points de coupure d'une chaîne : les flèches s'il y en a, sinon les « = »."""
    rels = top_level_relations(tex)
    arrows = [r for r in rels if r[2] in ARROWS]
    return arrows if arrows else rels


def top_level_relations(tex):
    """Positions (début, fin, symbole) des relations hors accolades et \\left…\\right."""
    rels = []
    depth = 0
    i = 0
    n = len(tex)
    while i < n:
        if tex.startswith("\\left", i) and not tex.startswith("\\leftarrow", i):
            depth += 1
            i += 5
            continue
        if tex.startswith("\\right", i) and not tex.startswith("\\rightarrow", i):
            depth = max(0, depth - 1)
            i += 6
            continue
        c = tex[i]
        if c == "\\":
            m = re.match(r"\\[A-Za-z]+", tex[i:])
            if m:
                word = m.group(0)
                if depth == 0 and word in ARROWS:
                    rels.append((i, i + len(word), word))
                i += len(word)
                continue
            i += 2
            continue
        if c in "{[(":
            depth += 1 if c == "{" else 0
        elif c == "}":
            depth = max(0, depth - 1)
        elif c == "=" and depth == 0:
            prev = tex[i - 1] if i > 0 else ""
            if prev not in "<>!:":
                rels.append((i, i + 1, "="))
        i += 1
    return rels


def to_aligned(tex):
    """Chaîne d'égalités -> environnement aligned (une égalité par ligne)."""
    rels = chain_relations(tex)
    if not rels:
        return tex
    # « A = …, \quad B = … et C = … » : plusieurs définitions côte à côte, pas une chaîne
    if re.search(r"\\q?quad|\\text\{\s*(et|mais|ou)\s*\}", tex):
        return tex
    pieces = []
    last = 0
    lhs = tex[: rels[0][0]].strip()
    for k, (a, b, sym) in enumerate(rels):
        nxt = rels[k + 1][0] if k + 1 < len(rels) else len(tex)
        pieces.append((sym, tex[b:nxt].strip()))
    lines = []
    for k, (sym, rhs) in enumerate(pieces):
        rel = sym if sym != "=" else "="
        if k == 0:
            lines.append(f"{lhs} &{rel} {rhs}" if lhs else f"&{rel} {rhs}")
        else:
            lines.append(f"&{rel} {rhs}")
    return "\\begin{aligned}\n" + " \\\\\n".join(lines) + "\n\\end{aligned}"


def display_block(tex, chain_min_len=55):
    """Formule centrée ; les longues chaînes d'égalités passent en aligned."""
    t = strip_displaystyle(tex)
    rels = chain_relations(t)
    has_arrows = bool(rels) and rels[0][2] in ARROWS
    if "\\begin" not in t and len(t) >= chain_min_len and (len(rels) >= 2 or (has_arrows and len(t) >= 55)):
        t = to_aligned(t)
    if "\n" in t:
        return ["$$", t, "$$"]
    return [f"$${t}$$"]


# ---------------------------------------------------------------------------
#  HTML
# ---------------------------------------------------------------------------

def html_inline_to_text(fragment):
    """HTML en ligne -> texte du format (gras/italique conservés, reste retiré)."""
    s = fragment
    s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"<(strong|b)\b[^>]*>(.*?)</\1>", lambda m: f"**{m.group(2).strip()}**" if m.group(2).strip() else "", s, flags=re.I | re.S)
    s = re.sub(r"<(em|i)\b[^>]*>(.*?)</\1>", lambda m: f"*{m.group(2).strip()}*" if m.group(2).strip() else "", s, flags=re.I | re.S)
    s = re.sub(r"<code\b[^>]*>(.*?)</code>", lambda m: "`" + re.sub(r"<[^>]+>", "", m.group(1)).replace("`", "'") + "`", s, flags=re.I | re.S)
    s = re.sub(r"<sup\b[^>]*>(.*?)</sup>", r"$^{\1}$", s, flags=re.I | re.S)
    s = re.sub(r"<sub\b[^>]*>(.*?)</sub>", r"$_{\1}$", s, flags=re.I | re.S)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace("\u00a0", " ")
    return s


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = dict(attrs or {})
        self.children = []
        self.parent = parent

    @property
    def style(self):
        return (self.attrs.get("style") or "").lower().replace(" ", "")

    def text(self):
        return "".join(c if isinstance(c, str) else c.text() for c in self.children)

    def html(self):
        out = []
        for c in self.children:
            if isinstance(c, str):
                out.append(html.escape(c, quote=False))
            else:
                attrs = "".join(f' {k}="{html.escape(v or "")}"' for k, v in c.attrs.items())
                if c.tag in VOID:
                    out.append(f"<{c.tag}{attrs}>")
                else:
                    out.append(f"<{c.tag}{attrs}>{c.html()}</{c.tag}>")
        return "".join(out)

    def outer_html(self):
        attrs = "".join(f' {k}="{html.escape(v or "")}"' for k, v in self.attrs.items())
        if self.tag in VOID:
            return f"<{self.tag}{attrs}>"
        return f"<{self.tag}{attrs}>{self.html()}</{self.tag}>"

    def find_all(self, tag):
        res = []
        for c in self.children:
            if isinstance(c, Node):
                if c.tag == tag:
                    res.append(c)
                res.extend(c.find_all(tag))
        return res

    def elements(self):
        return [c for c in self.children if isinstance(c, Node)]


VOID = {"br", "img", "hr", "meta", "link", "input", "col"}


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root")
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


REAL_TAG_RE = re.compile(
    r"</?(?:br|span|div|p|strong|b|em|i|u|sup|sub|code|pre|li|ul|ol|table|thead|tbody|tr|td|th|a|img|font|hr|h[1-6])"
    r"(?:\s[^<>$]*)?/?>", re.I)


def protect_math_lt(fragment):
    """« < » d'une formule ($r<b$, $x<y$) lu comme une balise : on l'échappe."""
    out, last = [], 0
    for a, b in math_spans(fragment):
        out.append(fragment[last:a])
        seg = fragment[a:b]
        buf, i = [], 0
        while i < len(seg):
            if seg[i] == "<":
                m = REAL_TAG_RE.match(seg, i)
                if m:
                    buf.append(m.group(0))
                    i = m.end()
                    continue
                buf.append("&lt;")
            elif seg[i] == ">":
                buf.append("&gt;")
            else:
                buf.append(seg[i])
            i += 1
        out.append("".join(buf))
        last = b
    out.append(fragment[last:])
    return "".join(out)


def parse_html(fragment):
    b = TreeBuilder()
    b.feed(protect_math_lt(fragment))
    b.close()
    return b.root


# ---------------------------------------------------------------------------
#  Code
# ---------------------------------------------------------------------------

CODE_BG = ("#2c3e50", "#282a36", "#1e1e1e", "#263238", "#1e293b")


def is_code_style(style):
    st = (style or "").lower().replace(" ", "")
    return "monospace" in st or any(f"background:{c}" in st for c in CODE_BG)


def code_from_html(fragment):
    """HTML d'un bloc de code (spans colorés, <br>, &nbsp;) -> texte brut."""
    s = fragment
    if re.search(r"<br\s*/?>", s, re.I):
        s = s.replace("\r", "").replace("\n", "")
        s = re.sub(r"<br\s*/?>", "\n", s, flags=re.I)
    s = re.sub(r"</(p|div|li)>", "\n", s, flags=re.I)
    s = re.sub(r"<[^>]+>", "", s)
    s = html.unescape(s).replace(" ", " ").replace("\t", "    ")
    lines = s.split("\n")
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    ind = min((len(l) - len(l.lstrip(" ")) for l in lines if l.strip()), default=0)
    return "\n".join(l[ind:].rstrip() for l in lines)


def code_fence(code, lang="python"):
    return ["", f"```{lang}", *code.split("\n"), "```", ""]


# ---------------------------------------------------------------------------
#  Tableaux
# ---------------------------------------------------------------------------

def cell_tex(text):
    """Contenu d'une cellule -> LaTeX sans les $ (pour un tableau tkz-tab)."""
    t = text.strip()
    inner = math_only(t)
    if inner is not None:
        return strip_displaystyle(inner)
    return t


ARROW_UP = {"↗", "\\nearrow", "nearrow"}
ARROW_DOWN = {"↘", "\\searrow", "searrow"}
ARROW_FLAT = {"→", "\\rightarrow", "\\to", "rightarrow"}


def arrow_of(text):
    t = text.strip().strip("$").strip()
    if t in ARROW_UP:
        return "up"
    if t in ARROW_DOWN:
        return "down"
    if t in ARROW_FLAT:
        return "flat"
    return None


def _abs_divs(cell):
    """Valeurs placées en position absolue dans une cellule (asymptotes)."""
    res = []
    for d in cell.find_all("div") + cell.find_all("span"):
        st = d.style
        if "position:absolute" not in st:
            continue
        vert = "top" if "top:" in st else "bottom" if "bottom:" in st else "middle"
        horiz = "left" if "left:" in st else "right" if "right:" in st else "center"
        res.append((horiz, vert, cell_tex(d.text())))
    return res


def table_rows(table):
    rows = []
    for tr in table.find_all("tr"):
        cells = [c for c in tr.elements() if c.tag in ("td", "th")]
        rows.append(cells)
    return rows


def convert_variation_table(table, warnings):
    """Tableau HTML (générateur historique) -> lignes `::: tableau` ou None."""
    rows = table_rows(table)
    if len(rows) < 2:
        return None
    head = rows[0]
    if not head or cell_tex(head[0].text()) not in ("x", "t", "n"):
        return None
    m = len(head) - 1
    if m < 3 or m % 2 == 0:
        return None
    n = (m + 1) // 2
    xs = [cell_tex(head[1 + 2 * k].text()) for k in range(n)]
    if any(not cell_tex(head[2 + 2 * k].text()) == "" for k in range(n - 1)):
        return None
    out = [f"x : {', '.join(xs)}"] if cell_tex(head[0].text()) == "x" else [f"{cell_tex(head[0].text())} : {', '.join(xs)}"]

    for row in rows[1:]:
        if len(row) != len(head):
            warnings.append("ligne de tableau de longueur différente")
            return None
        label = cell_tex(row[0].text())
        slots = row[1:]
        texts = [s.text().strip() for s in slots]
        arrows = [arrow_of(texts[s]) if s % 2 == 1 else None for s in range(m)]
        has_abs = any(_abs_divs(slots[s]) for s in range(0, m, 2))
        if any(arrows) or has_abs:
            entries = []
            for k in range(n):
                cell = slots[2 * k]
                before = arrows[2 * k - 1] if k > 0 else None
                after = arrows[2 * k + 1] if k < n - 1 else None
                divs = _abs_divs(cell)
                if divs:
                    left = next((d for d in divs if d[0] == "left"), None)
                    right = next((d for d in divs if d[0] == "right"), None)
                    sg = lambda d: "+" if d[1] == "top" else "-"
                    if left and right:
                        entries.append(f"{sg(left)}D{sg(right)}/{left[2]}/{right[2]}")
                    elif right:
                        entries.append(f"D{sg(right)}/{right[2]}")
                    elif left:
                        entries.append(f"{sg(left)}D/{left[2]}")
                    else:
                        entries.append(f"{sg(divs[0])}/{divs[0][2]}")
                    continue
                val = cell_tex(cell.text())
                if before == "up" and after == "down":
                    pos = "+"
                elif before == "down" and after == "up":
                    pos = "-"
                elif before is None and after:
                    pos = "-" if after == "up" else "+" if after == "down" else None
                elif after is None and before:
                    pos = "+" if before == "up" else "-" if before == "down" else None
                elif before == after and before in ("up", "down"):
                    # valeur intermédiaire : sur la flèche (=), ou flèche continue (R)
                    entries.append(f"=/{val}" if val else "R")
                    continue
                else:
                    pos = None
                if pos is None:
                    if before == "flat" or after == "flat":
                        pos = "+"
                    else:
                        warnings.append(f"position indéterminée pour « {val} »")
                        return None
                entries.append(f"{pos}/{val}")
            out.append(f"{label} : {', '.join(entries)}")
        else:
            toks = []
            for s in range(m):
                t = cell_tex(texts[s]).replace(" ", "")
                if s % 2 == 0:
                    if t in ("0",):
                        toks.append("z")
                    elif t in ("||", "\\|", "\\parallel", "|"):
                        toks.append("d")
                    elif t in ("+", "-"):
                        # un signe sous une borne : il appartient à l'intervalle voisin
                        toks.append("")
                    else:
                        toks.append(cell_tex(texts[s]))
                elif t in ("||", "\\|", "|", "\\parallel"):
                    toks.append("h")  # fonction non définie sur l'intervalle
                else:
                    toks.append(t if t in ("+", "-", "") else cell_tex(texts[s]))
            out.append(f"{label} : {', '.join(toks)}")
    return ["::: tableau", *(line.rstrip() for line in out), ":::"]


def convert_generic_table(table, warnings):
    """Tableau HTML quelconque -> tableau en barres verticales."""
    rows = table_rows(table)
    if not rows:
        return []
    if any(c.attrs.get("rowspan") or c.attrs.get("colspan") for r in rows for c in r):
        warnings.append("tableau avec cellules fusionnées (fusion ignorée)")

    def cell(c):
        frag = re.sub(r"<br\s*/?>", "\u0001BR\u0001", c.html(), flags=re.I)
        t = html_inline_to_text(frag)
        t = re.sub(r"\s+", " ", t).strip()
        t = re.sub(r"\s*\u0001BR\u0001\s*", " <br> ", t).strip()
        t = re.sub(r"^(<br>\s*)+|(\s*<br>)+$", "", t).strip()
        t = strip_emojis(t)
        return t.replace("|", "\\|") if "$" not in t else t

    has_head = rows[0] and all(c.tag == "th" for c in rows[0]) or bool(table.find_all("thead"))
    width = max(len(r) for r in rows)
    lines = []
    for k, r in enumerate(rows):
        vals = [cell(c) for c in r] + [""] * (width - len(r))
        lines.append("| " + " | ".join(vals) + " |")
        if k == 0 and has_head:
            lines.append("|" + "|".join(["---"] * width) + "|")
    return lines


def convert_table_html(fragment, warnings):
    root = parse_html(fragment)
    tables = root.find_all("table")
    if not tables:
        return []
    table = tables[0]
    cells = [c for r in table_rows(table) for c in r]
    code_cells = [c for c in cells if is_code_style(c.style)]
    if code_cells and len(code_cells) == len([c for c in cells if c.text().strip()]):
        # tableau qui ne sert qu'à afficher du code
        out = []
        for c in code_cells:
            out += code_fence(code_from_html(c.html()))
        return out
    tv = convert_variation_table(table, warnings)
    if tv:
        return tv
    return convert_generic_table(table, warnings)
