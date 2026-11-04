# -*- coding: utf-8 -*-
"""Scripts par blocs (style Scratch 3) : rendu matplotlib ET exécution pour contrôle.

Un même script sert à dessiner la figure de l'exercice et à vérifier les valeurs
annoncées dans le corrigé (cf. verifications/check_ch17.py).
"""
import math
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.patches import FancyBboxPatch, Polygon
from matplotlib.textpath import TextPath

# ---------------------------------------------------------------- expressions

def V(n):
    return ("var", n)


def T(s):
    return ("txt", s)


def P(n):
    return ("param", n)


ANS = ("ans",)


def RND(a, b):
    return ("rand", a, b)


def op(s, a, b):
    return ("op", s, a, b)


def cmp(s, a, b):
    return ("cmp", s, a, b)


# ---------------------------------------------------------------- style

FONT = FontProperties(family="DejaVu Sans", weight="bold")
FS = 10.5
COL = {
    "events": ("#FFBF00", "#CC9900"),
    "control": ("#FFAB19", "#CF8B17"),
    "motion": ("#4C97FF", "#3373CC"),
    "looks": ("#9966FF", "#774DCB"),
    "sensing": ("#5CB1D6", "#2E8EB8"),
    "operators": ("#59C059", "#389438"),
    "variables": ("#FF8C1A", "#DB6E00"),
    "pen": ("#0FBD8C", "#0B8E69"),
    "custom": ("#FF6680", "#FF4D6A"),
}
INK = "#575E75"
N1, N2, N3, N4, ND = 0.10, 0.15, 0.34, 0.39, 0.055
ARM = 0.20
GAP = 0.065
HMIN = 0.46


def tw(s):
    if not s:
        return 0.0
    return TextPath((0, 0), s, size=FS, prop=FONT).get_extents().width / 72 + 0.02


def fmt(v):
    if isinstance(v, float):
        if v.is_integer():
            v = int(v)
        else:
            return f"{v}".replace(".", ",")
    return str(v)


# ---------------------------------------------------------------- mesure / dessin des jetons

def _expr_tokens(e):
    tag = e[0]
    if tag == "rand":
        return "operators", "oval", [("t", "nombre aléatoire entre"), ("e", e[1]), ("t", "et"),
                                     ("e", e[2])]
    if tag == "op":
        sym = {"*": "*", "/": "/", "+": "+", "-": "-", "mod": "modulo"}[e[1]]
        return "operators", "oval", [("e", e[2]), ("t", sym), ("e", e[3])]
    if tag == "cmp":
        return "operators", "hex", [("e", e[2]), ("t", e[1]), ("e", e[3])]
    if tag in ("and", "or"):
        return "operators", "hex", [("e", e[1]), ("t", "et" if tag == "and" else "ou"),
                                    ("e", e[2])]
    if tag == "not":
        return "operators", "hex", [("t", "non"), ("e", e[1])]
    raise ValueError(e)


def leaf(e):
    """(texte, catégorie ou None pour un champ blanc)"""
    if isinstance(e, (int, float)):
        return fmt(e), None
    tag = e[0]
    if tag == "txt":
        return e[1], None
    if tag == "var":
        return e[1], "variables"
    if tag == "ans":
        return "réponse", "sensing"
    if tag == "param":
        return e[1], "custom"
    return None


def eh(e):
    if leaf(e) is not None:
        return 0.27
    _, _, toks = _expr_tokens(e)
    return max([eh(t[1]) + 0.07 for t in toks if t[0] == "e"] + [0.30])


def ew(e):
    lf = leaf(e)
    h = eh(e)
    if lf is not None:
        return max(tw(lf[0]) + 0.20, h)
    _, shape, toks = _expr_tokens(e)
    inner = toks_w(toks)
    return inner + (h if shape == "hex" else 0.16)


def tok_w(t):
    k = t[0]
    if k == "t":
        return tw(t[1])
    if k == "e":
        return ew(t[1])
    if k == "dd":
        return tw(t[1] + " ▾") + 0.18
    if k == "flag":
        return 0.22
    if k == "rot":
        return tw("↺")
    raise ValueError(t)


def toks_w(toks):
    return sum(tok_w(t) for t in toks) + GAP * (len(toks) - 1)


def toks_h(toks):
    return max([eh(t[1]) for t in toks if t[0] == "e"] + [0.27])


def draw_expr(ax, e, x, yc):
    lf = leaf(e)
    h, w = eh(e), ew(e)
    if lf is not None:
        txt, cat = lf
        fc, ec = ("white", "#c9cdd6") if cat is None else COL[cat]
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                    facecolor=fc, edgecolor=ec, lw=0.9, zorder=4))
        ax.text(x + w / 2, yc, txt, fontsize=FS, fontproperties=FONT, ha="center",
                va="center", color=INK if cat is None else "white", zorder=5)
        return w
    cat, shape, toks = _expr_tokens(e)
    fc, ec = COL[cat]
    if shape == "hex":
        pts = [(x, yc), (x + h / 2, yc + h / 2), (x + w - h / 2, yc + h / 2), (x + w, yc),
               (x + w - h / 2, yc - h / 2), (x + h / 2, yc - h / 2)]
        ax.add_patch(Polygon(pts, closed=True, facecolor=fc, edgecolor=ec, lw=0.9, zorder=3))
        x0 = x + h / 2
    else:
        ax.add_patch(FancyBboxPatch((x, yc - h / 2), w, h,
                                    boxstyle=f"round,pad=0,rounding_size={h / 2}",
                                    facecolor=fc, edgecolor=ec, lw=0.9, zorder=3))
        x0 = x + 0.08
    draw_toks(ax, toks, x0, yc, "white")
    return w


def draw_toks(ax, toks, x, yc, color="white", cat=None):
    for t in toks:
        k = t[0]
        if k == "t":
            ax.text(x, yc, t[1], fontsize=FS, fontproperties=FONT, ha="left", va="center",
                    color=color, zorder=5)
        elif k == "e":
            draw_expr(ax, t[1], x, yc)
        elif k == "dd":
            w = tok_w(t)
            fc, ec = COL[cat]
            ax.add_patch(FancyBboxPatch((x, yc - 0.135), w, 0.27,
                                        boxstyle="round,pad=0,rounding_size=0.06",
                                        facecolor=ec, edgecolor=ec, lw=0.9, zorder=4))
            ax.text(x + 0.09, yc, t[1] + " ▾", fontsize=FS, fontproperties=FONT, ha="left",
                    va="center", color="white", zorder=5)
        elif k == "flag":
            ax.plot([x + 0.05, x + 0.05], [yc - 0.11, yc + 0.11], color="#2E7D32", lw=1.6,
                    zorder=6)
            ax.add_patch(Polygon([(x + 0.05, yc + 0.11), (x + 0.21, yc + 0.06),
                                  (x + 0.05, yc + 0.0)], closed=True, facecolor="#4CBF56",
                                 edgecolor="#2E7D32", lw=1.0, zorder=6))
        elif k == "rot":
            ax.text(x, yc, "↺" if t[1] == "left" else "↻", fontsize=FS + 1,
                    fontproperties=FONT, ha="left", va="center", color=color, zorder=5)
        x += tok_w(t) + GAP


# ---------------------------------------------------------------- blocs

def block_spec(b):
    """(catégorie, forme, jetons) ; forme : stack | hat | c | ce."""
    k = b[0]
    E = lambda e: ("e", e if not isinstance(e, str) else T(e))  # noqa: E731
    if k == "flag":
        return "events", "hat", [("t", "quand"), ("flag",), ("t", "est cliqué")]
    if k == "recv":
        return "events", "hat", [("t", "quand je reçois"), ("dd", b[1])]
    if k == "define":
        return "custom", "hat", [("t", "définir"), ("t", b[1])] + [("e", P(p)) for p in b[2]]
    if k == "set":
        return "variables", "stack", [("t", "mettre"), ("dd", b[1]), ("t", "à"), E(b[2])]
    if k == "change":
        return "variables", "stack", [("t", "ajouter"), E(b[2]), ("t", "à"), ("dd", b[1])]
    if k == "ask":
        return "sensing", "stack", [("t", "demander"), E(b[1]), ("t", "et attendre")]
    if k == "say":
        return "looks", "stack", [("t", "dire"), E(b[1])]
    if k == "saysec":
        return "looks", "stack", [("t", "dire"), E(b[1]), ("t", "pendant"), E(b[2]),
                                  ("t", "secondes")]
    if k == "goto":
        return "motion", "stack", [("t", "aller à x :"), E(b[1]), ("t", "y :"), E(b[2])]
    if k == "point":
        return "motion", "stack", [("t", "s'orienter à"), E(b[1])]
    if k == "move":
        return "motion", "stack", [("t", "avancer de"), E(b[1])]
    if k in ("left", "right"):
        return "motion", "stack", [("t", "tourner"), ("rot", k), ("t", "de"), E(b[1]),
                                   ("t", "degrés")]
    if k == "pendown":
        return "pen", "stack", [("t", "stylo en position d'écriture")]
    if k == "penup":
        return "pen", "stack", [("t", "relever le stylo")]
    if k == "clear":
        return "pen", "stack", [("t", "effacer tout")]
    if k == "call":
        return "custom", "stack", [("t", b[1])] + [E(a) for a in b[2]]
    if k == "broadcast":
        return "events", "stack", [("t", "envoyer à tous"), ("dd", b[1])]
    if k == "broadcastwait":
        return "events", "stack", [("t", "envoyer à tous"), ("dd", b[1]), ("t", "et attendre")]
    if k == "repeat":
        return "control", "c", [("t", "répéter"), E(b[1]), ("t", "fois")]
    if k == "until":
        return "control", "c", [("t", "répéter jusqu'à"), E(b[1])]
    if k == "if":
        return "control", "c", [("t", "si"), E(b[1]), ("t", "alors")]
    if k == "ifelse":
        return "control", "ce", [("t", "si"), E(b[1]), ("t", "alors")]
    raise ValueError(b)


def _top(x, y, notch=True):
    if not notch:
        return [(x, y)]
    return [(x, y), (x + N1, y), (x + N2, y - ND), (x + N3, y - ND), (x + N4, y)]


def _tab_left(x0, y):
    """bord inférieur parcouru vers la gauche, avec un ergot vers le bas à partir de x0"""
    return [(x0 + N4, y), (x0 + N3, y - ND), (x0 + N2, y - ND), (x0 + N1, y), (x0, y)]


def stack_h(blocks):
    return sum(block_h(b) for b in blocks)


def block_h(b):
    cat, shape, toks = block_spec(b)
    h = max(HMIN, toks_h(toks) + 0.16)
    if shape == "hat":
        return h + 0.10
    if shape == "c":
        return h + max(stack_h(b[2]), 0.28) + 0.30
    if shape == "ce":
        return h + max(stack_h(b[2]), 0.28) + 0.40 + max(stack_h(b[3]), 0.28) + 0.30
    return h


def draw_block(ax, b, x, y):
    """Dessine le bloc b, coin haut-gauche (x, y). Retourne (y_bas, x_max)."""
    cat, shape, toks = block_spec(b)
    fc, ec = COL[cat]
    h = max(HMIN, toks_h(toks) + 0.16)
    w = max(toks_w(toks) + 0.26, 1.15)
    kw = dict(closed=True, facecolor=fc, edgecolor=ec, lw=1.0, joinstyle="round", zorder=2)
    if shape == "stack":
        pts = _top(x, y) + [(x + w, y), (x + w, y - h)] + _tab_left(x, y - h)
        ax.add_patch(Polygon(pts, **kw))
        draw_toks(ax, toks, x + 0.12, y - h / 2, "white", cat)
        return y - h, x + w
    if shape == "hat":
        w = max(w, 1.35)
        bump = [(x + 1.1 * t, y + 0.20 * math.sin(math.pi * t)) for t in
                [i / 30 for i in range(31)]]
        yb = y - h - 0.10
        pts = bump + [(x + w, y), (x + w, yb)] + _tab_left(x, yb)
        ax.add_patch(Polygon(pts, **kw))
        draw_toks(ax, toks, x + 0.12, y - (h + 0.10) / 2 - 0.02, "white", cat)
        return yb, x + w
    # blocs en C
    wb = 1.25
    y1 = y - h
    xi = x + ARM
    pts = _top(x, y) + [(x + w, y), (x + w, y1)] + _tab_left(xi, y1)
    yy, xmax = y1, x + w
    for t in b[2]:
        yy, xm = draw_block(ax, t, xi, yy)
        xmax = max(xmax, xm)
    yy = min(yy, y1 - 0.28)
    pts += [(xi, yy)]
    if shape == "ce":
        hm = 0.40
        pts += _top(xi, yy)[1:] + [(x + wb, yy), (x + wb, yy - hm)] + _tab_left(xi, yy - hm)
        ax.text(x + 0.12, yy - hm / 2, "sinon", fontsize=FS, fontproperties=FONT, ha="left",
                va="center", color="white", zorder=5)
        ys = yy - hm
        yy = ys
        for t in b[3]:
            yy, xm = draw_block(ax, t, xi, yy)
            xmax = max(xmax, xm)
        yy = min(yy, ys - 0.28)
        pts += [(xi, yy)]
    yb = yy - 0.30
    pts += _top(xi, yy)[1:] + [(x + wb, yy), (x + wb, yb)] + _tab_left(x, yb)
    ax.add_patch(Polygon(pts, **kw))
    draw_toks(ax, toks, x + 0.12, y - h / 2, "white", cat)
    return yb, xmax


def draw_script(ax, blocks, x, y):
    xmax = x
    for b in blocks:
        y, xm = draw_block(ax, b, x, y)
        xmax = max(xmax, xm)
    return y, xmax


def render(path, scripts, titles=None, gap=0.55):
    """scripts : liste de scripts (listes de blocs) dessinés côte à côte."""
    fig = plt.figure(figsize=(30, 30))
    ax = fig.add_axes([0, 0, 1, 1])
    x, ymin, xmax = 0.15, 0.0, 0.0
    top = -0.45 if titles else -0.30
    for i, s in enumerate(scripts):
        if titles and titles[i]:
            ax.text(x, -0.12, titles[i], fontsize=FS + 1.5, fontproperties=FONT, ha="left",
                    va="center", color="#2c3e50")
        yb, xm = draw_script(ax, s, x, top)
        ymin, xmax = min(ymin, yb), max(xmax, xm)
        x = xm + gap
    W, H = xmax + 0.25, -ymin + 0.25
    fig.set_size_inches(W, H)
    ax.set_xlim(0, W)
    ax.set_ylim(ymin - 0.2, 0.05)
    ax.axis("off")
    fig.savefig(path, dpi=170, facecolor="white")
    plt.close(fig)
    print("OK", os.path.basename(path))


# ---------------------------------------------------------------- exécution

class Stop(Exception):
    pass


def run(scripts, inputs=(), seed=0, max_steps=500000):
    """Exécute un projet (liste de scripts). Retourne un dict :
    out (valeurs dites), env, segs (segments tracés), pos, dir, steps."""
    rng = random.Random(seed)
    env, out, segs = {}, [], []
    st = {"x": 0.0, "y": 0.0, "dir": 90.0, "pen": False, "answer": "", "steps": 0}
    it = iter(inputs)
    procs, recv, flags = {}, {}, []
    for s in scripts:
        h = s[0]
        if h[0] == "define":
            procs[h[1]] = (h[2], s[1:])
        elif h[0] == "recv":
            recv.setdefault(h[1], []).append(s[1:])
        elif h[0] == "flag":
            flags.append(s[1:])
        else:
            flags.append(s)

    def num(v):
        if isinstance(v, str):
            try:
                f = float(v.replace(",", "."))
                return int(f) if f.is_integer() else f
            except ValueError:
                return v
        return v

    def ev(e, loc):
        if isinstance(e, (int, float)):
            return e
        if isinstance(e, str):
            return num(e)
        t = e[0]
        if t == "txt":
            return num(e[1])
        if t == "var":
            return env[e[1]]
        if t == "param":
            return loc[e[1]]
        if t == "ans":
            return num(st["answer"])
        if t == "rand":
            return rng.randint(ev(e[1], loc), ev(e[2], loc))
        if t == "op":
            a, b = ev(e[2], loc), ev(e[3], loc)
            r = {"+": lambda: a + b, "-": lambda: a - b, "*": lambda: a * b,
                 "/": lambda: a / b, "mod": lambda: a - math.floor(a / b) * b}[e[1]]()
            if isinstance(r, float) and r.is_integer():
                r = int(r)
            return r
        if t == "cmp":
            a, b = ev(e[2], loc), ev(e[3], loc)
            if not (isinstance(a, (int, float)) and isinstance(b, (int, float))):
                a, b = str(a).lower(), str(b).lower()
            if e[1] == "<":
                return a < b
            if e[1] == ">":
                return a > b
            return a == b
        if t == "and":
            return ev(e[1], loc) and ev(e[2], loc)
        if t == "or":
            return ev(e[1], loc) or ev(e[2], loc)
        if t == "not":
            return not ev(e[1], loc)
        raise ValueError(e)

    def go(nx, ny):
        nx, ny = round(nx, 9), round(ny, 9)
        if st["pen"]:
            segs.append(((st["x"], st["y"]), (nx, ny)))
        st["x"], st["y"] = nx, ny

    def exe(blocks, loc):
        for b in blocks:
            st["steps"] += 1
            if st["steps"] > max_steps:
                raise Stop("boucle non terminée")
            k = b[0]
            if k == "set":
                env[b[1]] = ev(b[2], loc)
            elif k == "change":
                env[b[1]] = env[b[1]] + ev(b[2], loc)
            elif k == "ask":
                st["answer"] = next(it)
            elif k in ("say", "saysec"):
                out.append(ev(b[1], loc))
            elif k == "goto":
                go(ev(b[1], loc), ev(b[2], loc))
            elif k == "point":
                st["dir"] = ev(b[1], loc)
            elif k == "move":
                d = ev(b[1], loc)
                a = math.radians(st["dir"])
                go(st["x"] + d * math.sin(a), st["y"] + d * math.cos(a))
            elif k == "left":
                st["dir"] -= ev(b[1], loc)
            elif k == "right":
                st["dir"] += ev(b[1], loc)
            elif k == "pendown":
                st["pen"] = True
            elif k == "penup":
                st["pen"] = False
            elif k == "clear":
                segs.clear()
            elif k == "call":
                params, body = procs[b[1]]
                exe(body, dict(zip(params, [ev(a, loc) for a in b[2]])))
            elif k in ("broadcast", "broadcastwait"):
                for body in recv.get(b[1], []):
                    exe(body, {})
            elif k == "repeat":
                for _ in range(int(ev(b[1], loc))):
                    exe(b[2], loc)
            elif k == "until":
                while not ev(b[1], loc):
                    st["steps"] += 1
                    if st["steps"] > max_steps:
                        raise Stop("boucle non terminée")
                    exe(b[2], loc)
            elif k == "if":
                if ev(b[1], loc):
                    exe(b[2], loc)
            elif k == "ifelse":
                exe(b[2] if ev(b[1], loc) else b[3], loc)
            else:
                raise ValueError(b)

    for body in flags:
        exe(body, {})
    return {"out": out, "env": env, "segs": segs, "pos": (st["x"], st["y"]),
            "dir": st["dir"], "steps": st["steps"]}
